"""One chat turn: intake → ask for missing slots, or gather writers → picker."""

from __future__ import annotations

import asyncio
import traceback
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable

from agent.brief import EmailBrief, merge_briefs, with_status
from agent.guardrails import assert_brief_complete
from agent.providers import (
    DEFAULT_ORCHESTRATION,
    DEFAULT_WRITER_PROVIDER,
    MissingApiKeyError,
    normalize_orchestration,
    normalize_writer_provider,
    require_openai_api_key,
    resolve_writer_model,
)
from agent.runtime import MODEL_NAME

ExtractBrief = Callable[[str, list, EmailBrief], Awaitable[EmailBrief]]
AskForMissing = Callable[[str, list, EmailBrief], Awaitable[str]]
DraftAndPick = Callable[[str, EmailBrief], Awaitable[tuple[str, list[str]]]]
PresentDraft = Callable[[str, list[str], EmailBrief], Awaitable[str]]


@dataclass
class StudioContext:
    """Passed to Runner.run so writer/picker input guardrails can see the brief."""

    brief: EmailBrief


@dataclass
class StudioState:
    brief: EmailBrief = field(default_factory=EmailBrief)
    session_id: str = "sales-studio"
    _session: Any = field(default=None, repr=False)

    @property
    def session(self):
        if self._session is None:
            from agents import SQLiteSession

            self._session = SQLiteSession(self.session_id)
        return self._session


@dataclass
class StudioDeps:
    extract_brief: ExtractBrief
    ask_for_missing: AskForMissing
    draft_and_pick: DraftAndPick
    present_draft: PresentDraft


def format_history(history: list | None) -> str:
    if not history:
        return "(none)"
    lines: list[str] = []
    for item in history:
        if isinstance(item, dict):
            role = item.get("role", "user")
            content = item.get("content", "")
            lines.append(f"{role}: {content}")
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            lines.append(f"user: {item[0]}")
            lines.append(f"assistant: {item[1]}")
    return "\n".join(lines) if lines else "(none)"


def intake_prompt(message: str, history: list, stored: EmailBrief) -> str:
    return (
        "Known brief so far:\n"
        f"{with_status(stored).model_dump_json()}\n\n"
        "Recent conversation:\n"
        f"{format_history(history)}\n\n"
        "Latest user message:\n"
        f"{message}\n\n"
        "Extract any new field values. Leave unknown fields as null."
    )


def writer_prompt(brief: EmailBrief, user_message: str) -> str:
    return (
        f"From {brief.author} to {brief.receiver}. "
        f"Field: {brief.field}. Purpose: {brief.purpose}.\n"
        f"User request: {user_message}\n"
        "Draft a short sales email. Use the real names. No placeholders."
    )


def picker_prompt(brief: EmailBrief, labeled_drafts: list[tuple[str, str]]) -> str:
    blocks = [f"{name}:\n{draft}" for name, draft in labeled_drafts]
    return (
        "Pick the best draft for this brief:\n"
        f"From {brief.author} to {brief.receiver}. "
        f"Field: {brief.field}. Purpose: {brief.purpose}.\n\n"
        "Draft Emails:\n\n" + "\n\n".join(blocks)
    )


def _output_text(result: Any) -> str:
    output = getattr(result, "final_output", result)
    return output if isinstance(output, str) else str(output)


def format_unexpected_error(exc: BaseException) -> str:
    """Turn an API/runtime exception into a chat message (not Gradio's generic Error)."""
    name = type(exc).__name__
    message = str(exc).strip() or "(no message)"
    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        nested = body.get("error", body)
        extra = nested.get("message") if isinstance(nested, dict) else None
        if extra and extra not in message:
            message = f"{message}\n{extra}"
    return (
        "Sales Email Studio hit an unexpected error on this turn.\n\n"
        f"{name}: {message}\n\n"
        "Your brief is still saved. Try again, switch Settings, or check the model/API key."
    )


async def extract_brief(
    message: str,
    history: list,
    stored: EmailBrief,
    *,
    agent: Any,
    runner: Any | None = None,
) -> EmailBrief:
    from agents import Runner

    run = runner or Runner.run
    result = await run(agent, intake_prompt(message, history, stored))
    incoming = result.final_output
    if not isinstance(incoming, EmailBrief):
        incoming = EmailBrief.model_validate(incoming)
    return incoming


async def ask_for_missing(
    message: str,
    history: list,
    brief: EmailBrief,
    *,
    agent: Any,
    session: Any | None = None,
    runner: Any | None = None,
) -> str:
    from agents import Runner

    run = runner or Runner.run
    missing = ", ".join(brief.missing_fields)
    prompt = (
        f"The user said: {message}\n\n"
        f"The email brief is still incomplete. Missing: {missing}.\n"
        "Ask for those fields only. Do not draft an email."
    )
    kwargs: dict[str, Any] = {}
    if session is not None:
        kwargs["session"] = session
    result = await run(agent, prompt, **kwargs)
    return _output_text(result)


async def draft_and_pick_code(
    message: str,
    brief: EmailBrief,
    *,
    writers: tuple[Any, Any, Any],
    picker: Any,
    runner: Any | None = None,
    span: Any | None = None,
) -> tuple[str, list[str]]:
    """Parallel writers then picker. Raises IncompleteBriefError if gated."""
    from contextlib import nullcontext

    complete = assert_brief_complete(brief)
    if runner is None:
        from agents import Runner

        runner = Runner.run
    if span is None:
        try:
            from agents import trace

            span = trace("sales-studio-draft-code")
        except ImportError:
            span = nullcontext()
    context = StudioContext(brief=complete)
    prompt = writer_prompt(complete, message)
    writer_names = [getattr(w, "name", f"writer-{i}") for i, w in enumerate(writers)]

    with span:
        results = await asyncio.gather(
            *(runner(writer, prompt, context=context) for writer in writers)
        )
        labeled = [
            (writer_names[i], _output_text(results[i])) for i in range(len(writers))
        ]
        picked = await runner(picker, picker_prompt(complete, labeled), context=context)

    return _output_text(picked), writer_names


draft_and_pick = draft_and_pick_code


def llm_manager_prompt(brief: EmailBrief, user_message: str) -> str:
    return (
        writer_prompt(brief, user_message)
        + "\nCall all three writer tools, pick the best draft, and present it to the user."
    )


async def draft_and_pick_llm(
    message: str,
    brief: EmailBrief,
    *,
    manager: Any,
    runner: Any | None = None,
    span: Any | None = None,
) -> tuple[str, list[str]]:
    """LLM orchestration: manager calls writers as tools. Raises if gated."""
    from contextlib import nullcontext

    complete = assert_brief_complete(brief)
    if runner is None:
        from agents import Runner

        runner = Runner.run
    if span is None:
        try:
            from agents import trace

            span = trace("sales-studio-draft-llm")
        except ImportError:
            span = nullcontext()
    context = StudioContext(brief=complete)
    with span:
        result = await runner(manager, llm_manager_prompt(complete, message), context=context)
    return _output_text(result), [
        "Friendly Writer",
        "Professional Writer",
        "Creative Writer",
    ]


async def present_draft(
    winning: str,
    considered: list[str],
    brief: EmailBrief,
    *,
    agent: Any,
    session: Any | None = None,
    runner: Any | None = None,
) -> str:
    from agents import Runner

    run = runner or Runner.run
    styles = ", ".join(considered)
    prompt = (
        "Present this winning sales email to the user. Keep the email intact.\n"
        f"Optionally one sentence that other styles were considered ({styles}).\n"
        f"Brief: from {brief.author} to {brief.receiver}; "
        f"field {brief.field}; purpose {brief.purpose}.\n\n"
        f"Winning draft:\n{winning}"
    )
    kwargs: dict[str, Any] = {}
    if session is not None:
        kwargs["session"] = session
    result = await run(agent, prompt, **kwargs)
    return _output_text(result)


async def handle_turn(
    message: str,
    history: list | None,
    state: StudioState,
    deps: StudioDeps,
) -> str:
    incoming = await deps.extract_brief(message, history or [], state.brief)
    state.brief = merge_briefs(state.brief, incoming)

    if not state.brief.is_complete:
        return await deps.ask_for_missing(message, history or [], state.brief)

    winning, considered = await deps.draft_and_pick(message, state.brief)
    return await deps.present_draft(winning, considered, state.brief)


def production_deps(
    model: str = MODEL_NAME,
    state: StudioState | None = None,
    writer_provider: str = DEFAULT_WRITER_PROVIDER,
    orchestration: str = DEFAULT_ORCHESTRATION,
) -> StudioDeps:
    from agent.agents import build_llm_manager, build_studio_agents

    provider = normalize_writer_provider(writer_provider)
    mode = normalize_orchestration(orchestration)
    require_openai_api_key()
    studio = build_studio_agents(
        model=model,
        writer_model=resolve_writer_model(provider),
    )
    session = state.session if state is not None else None

    async def _extract(message: str, history: list, stored: EmailBrief) -> EmailBrief:
        return await extract_brief(message, history, stored, agent=studio.intake)

    async def _ask(message: str, history: list, brief: EmailBrief) -> str:
        return await ask_for_missing(
            message, history, brief, agent=studio.manager, session=session
        )

    if mode == "code":

        async def _draft(message: str, brief: EmailBrief) -> tuple[str, list[str]]:
            return await draft_and_pick_code(
                message, brief, writers=studio.writers, picker=studio.picker
            )

        async def _present(winning: str, considered: list[str], brief: EmailBrief) -> str:
            return await present_draft(
                winning, considered, brief, agent=studio.manager, session=session
            )
    else:
        llm_manager = build_llm_manager(studio.writers, model=model)

        async def _draft(message: str, brief: EmailBrief) -> tuple[str, list[str]]:
            return await draft_and_pick_llm(message, brief, manager=llm_manager)

        async def _present(winning: str, considered: list[str], brief: EmailBrief) -> str:
            return winning

    return StudioDeps(
        extract_brief=_extract,
        ask_for_missing=_ask,
        draft_and_pick=_draft,
        present_draft=_present,
    )


def build_chat(
    deps: StudioDeps | None = None,
    state: StudioState | None = None,
    model: str = MODEL_NAME,
):
    """Gradio ChatInterface callback (async). Accepts provider and orchestration radios."""
    state = state or StudioState()
    injected = deps

    async def chat(
        message,
        history,
        writer_provider: str = "OpenAI",
        orchestration: str = "LLM",
    ):
        try:
            turn_deps = injected or production_deps(
                model=model,
                state=state,
                writer_provider=writer_provider,
                orchestration=orchestration,
            )
            return await handle_turn(message, history, state, turn_deps)
        except MissingApiKeyError as exc:
            return str(exc)
        except Exception as exc:
            traceback.print_exc()
            return format_unexpected_error(exc)

    return chat
