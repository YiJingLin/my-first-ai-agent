"""Six Sales Email Studio agents. Only the Sales Manager talks to the user."""

from __future__ import annotations

from dataclasses import dataclass

from agents import Agent

from agent.brief import EmailBrief
from agent.guardrails import get_intake_guardrail
from agent.runtime import MODEL_NAME

INTAKE_INSTRUCTIONS = """
You extract a sales-email brief from the conversation.
Fill only fields that are clearly stated. Use null for unknown.
Do not invent names, domains, or purposes.
Required fields: author (sender), receiver (recipient), field (domain/industry), purpose.
Set missing_fields to the required fields that are still unknown.
Set is_complete true only when all four required fields are present.
""".strip()

MANAGER_INSTRUCTIONS = """
You are a Sales Manager helping the user construct a sales email.
You never invent missing names, industry, or purpose.
If the brief is incomplete, ask only for the missing fields. Do not draft an email.
If you are given a winning draft, present it clearly and keep the email intact.
""".strip()

FRIENDLY_INSTRUCTIONS = """
You are a friendly and enthusiastic sales email writer.
Write persuasive outreach emails in a warm, conversational tone.
Use the real author and receiver names. Do not use placeholders like [Name].
""".strip()

PROFESSIONAL_INSTRUCTIONS = """
You are a concise and professional sales email writer.
Write directly to the point, using a formal and respectful business voice.
Use the real author and receiver names. Do not use placeholders like [Name].
""".strip()

CREATIVE_INSTRUCTIONS = """
You are a creative sales email writer who uses playful metaphors and humor.
Stay business-appropriate. Use the real author and receiver names.
Do not use placeholders like [Name].
""".strip()

PICKER_INSTRUCTIONS = """
You are an expert sales manager.
Review the candidate emails (friendly, professional, creative).
Evaluate persuasiveness, clarity, professionalism, and fit for the brief.
Return the best draft, with a brief explanation of your choice.
""".strip()


@dataclass(frozen=True)
class StudioAgents:
    manager: Agent
    intake: Agent
    friendly: Agent
    professional: Agent
    creative: Agent
    picker: Agent

    @property
    def writers(self) -> tuple[Agent, Agent, Agent]:
        return (self.friendly, self.professional, self.creative)


def build_studio_agents(model: str = MODEL_NAME) -> StudioAgents:
    intake_guardrail = get_intake_guardrail()
    return StudioAgents(
        manager=Agent(
            name="Sales Manager",
            instructions=MANAGER_INSTRUCTIONS,
            model=model,
        ),
        intake=Agent(
            name="Intake Checker",
            instructions=INTAKE_INSTRUCTIONS,
            model=model,
            output_type=EmailBrief,
        ),
        friendly=Agent(
            name="Friendly Writer",
            instructions=FRIENDLY_INSTRUCTIONS,
            model=model,
            input_guardrails=[intake_guardrail],
        ),
        professional=Agent(
            name="Professional Writer",
            instructions=PROFESSIONAL_INSTRUCTIONS,
            model=model,
            input_guardrails=[intake_guardrail],
        ),
        creative=Agent(
            name="Creative Writer",
            instructions=CREATIVE_INSTRUCTIONS,
            model=model,
            input_guardrails=[intake_guardrail],
        ),
        picker=Agent(
            name="Draft Picker",
            instructions=PICKER_INSTRUCTIONS,
            model=model,
            input_guardrails=[intake_guardrail],
        ),
    )
