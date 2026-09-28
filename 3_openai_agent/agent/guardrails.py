"""Intake gate: writers must not run until the brief is complete."""

from __future__ import annotations

from agent.brief import REQUIRED_FIELDS, EmailBrief, compute_missing, with_status


class IncompleteBriefError(ValueError):
    def __init__(self, missing_fields: list[str]):
        self.missing_fields = missing_fields
        super().__init__(f"Incomplete brief; missing: {', '.join(missing_fields)}")


def intake_tripwire(brief: EmailBrief | None) -> tuple[bool, list[str]]:
    """Return (should_block, missing_fields). Does not call an LLM."""
    if brief is None:
        return True, list(REQUIRED_FIELDS)
    missing = compute_missing(brief)
    return bool(missing), missing


def assert_brief_complete(brief: EmailBrief | None) -> EmailBrief:
    blocked, missing = intake_tripwire(brief)
    if blocked:
        raise IncompleteBriefError(missing)
    assert brief is not None
    return with_status(brief)


def get_intake_guardrail():
    """SDK @input_guardrail: trip if RunContext.brief is incomplete."""
    from agents import GuardrailFunctionOutput, input_guardrail

    @input_guardrail
    async def intake_guardrail(ctx, agent, input):
        brief = getattr(getattr(ctx, "context", None), "brief", None)
        blocked, missing = intake_tripwire(brief)
        return GuardrailFunctionOutput(
            output_info={"missing_fields": missing},
            tripwire_triggered=blocked,
        )

    return intake_guardrail
