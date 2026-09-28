"""Unit tests for chat-turn orchestration (mocked agent deps)."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from agent.brief import EmailBrief, with_status
from agent.guardrails import IncompleteBriefError
from contextlib import nullcontext

from agent.orchestrate import (
    StudioDeps,
    StudioState,
    draft_and_pick,
    handle_turn,
    picker_prompt,
    writer_prompt,
)


def _complete_brief() -> EmailBrief:
    return with_status(
        EmailBrief(
            author="Jordan",
            receiver="Priya",
            field="SaaS analytics",
            purpose="book a demo",
        )
    )


def test_incomplete_turn_asks_and_never_calls_writers():
    extract = AsyncMock(return_value=EmailBrief(author="Jordan"))
    ask = AsyncMock(return_value="Who should I address this to?")
    draft = AsyncMock(return_value=("should not run", ["Friendly Writer"]))
    present = AsyncMock(return_value="should not present")
    state = StudioState()
    deps = StudioDeps(
        extract_brief=extract,
        ask_for_missing=ask,
        draft_and_pick=draft,
        present_draft=present,
    )

    reply = asyncio.run(handle_turn("Help me write a sales email", [], state, deps))

    assert reply == "Who should I address this to?"
    assert state.brief.author == "Jordan"
    assert state.brief.is_complete is False
    ask.assert_awaited_once()
    draft.assert_not_called()
    present.assert_not_called()


def test_complete_turn_runs_draft_pipeline():
    extract = AsyncMock(return_value=_complete_brief())
    ask = AsyncMock(return_value="should not ask")
    draft = AsyncMock(return_value=("Best draft body", ["Friendly Writer", "Professional Writer"]))
    present = AsyncMock(return_value="Here is the winning email.")
    state = StudioState()
    deps = StudioDeps(
        extract_brief=extract,
        ask_for_missing=ask,
        draft_and_pick=draft,
        present_draft=present,
    )

    reply = asyncio.run(
        handle_turn("From Jordan to Priya, SaaS analytics, book a demo", [], state, deps)
    )

    assert reply == "Here is the winning email."
    assert state.brief.is_complete is True
    draft.assert_awaited_once()
    present.assert_awaited_once()
    ask.assert_not_called()


def test_second_turn_merges_until_complete_then_drafts():
    extract = AsyncMock(
        side_effect=[
            EmailBrief(author="Jordan", receiver="Priya"),
            EmailBrief(field="SaaS analytics", purpose="book a demo"),
        ]
    )
    ask = AsyncMock(return_value="What industry and purpose?")
    draft = AsyncMock(return_value=("draft", ["Friendly Writer"]))
    present = AsyncMock(return_value="presented")
    state = StudioState()
    deps = StudioDeps(
        extract_brief=extract,
        ask_for_missing=ask,
        draft_and_pick=draft,
        present_draft=present,
    )

    first = asyncio.run(handle_turn("I'm Jordan, writing to Priya", [], state, deps))
    assert first == "What industry and purpose?"
    draft.assert_not_called()

    second = asyncio.run(
        handle_turn("SaaS analytics, book a demo", [("I'm Jordan, writing to Priya", first)], state, deps)
    )
    assert second == "presented"
    assert state.brief.is_complete is True
    draft.assert_awaited_once()


def test_draft_and_pick_raises_before_runner_when_incomplete():
    runner = AsyncMock()
    writers = (MagicMock(name="Friendly Writer"), MagicMock(), MagicMock())

    with pytest.raises(IncompleteBriefError):
        asyncio.run(
            draft_and_pick(
                "write it",
                EmailBrief(author="Jordan"),
                writers=writers,
                picker=MagicMock(),
                runner=runner,
            )
        )

    runner.assert_not_called()


def test_draft_and_pick_gathers_writers_then_picker():
    runner = AsyncMock(
        side_effect=[
            MagicMock(final_output="friendly draft"),
            MagicMock(final_output="pro draft"),
            MagicMock(final_output="creative draft"),
            MagicMock(final_output="winning draft"),
        ]
    )
    friendly = MagicMock()
    friendly.name = "Friendly Writer"
    professional = MagicMock()
    professional.name = "Professional Writer"
    creative = MagicMock()
    creative.name = "Creative Writer"
    picker = MagicMock()
    picker.name = "Draft Picker"

    winning, considered = asyncio.run(
        draft_and_pick(
            "make it short",
            _complete_brief(),
            writers=(friendly, professional, creative),
            picker=picker,
            runner=runner,
            span=nullcontext(),
        )
    )

    assert winning == "winning draft"
    assert considered == ["Friendly Writer", "Professional Writer", "Creative Writer"]
    assert runner.await_count == 4
    writer_prompts = [call.args[1] for call in runner.await_args_list[:3]]
    assert all("Jordan" in prompt and "Priya" in prompt for prompt in writer_prompts)
    picker_input = runner.await_args_list[3].args[1]
    assert "friendly draft" in picker_input
    assert "pro draft" in picker_input
    assert "creative draft" in picker_input


def test_writer_and_picker_prompt_include_brief():
    brief = _complete_brief()
    wp = writer_prompt(brief, "make it shorter")
    assert "Jordan" in wp and "Priya" in wp
    assert "SaaS analytics" in wp
    assert "make it shorter" in wp

    pp = picker_prompt(brief, [("Friendly Writer", "hello")])
    assert "book a demo" in pp
    assert "Friendly Writer" in pp
    assert "hello" in pp
