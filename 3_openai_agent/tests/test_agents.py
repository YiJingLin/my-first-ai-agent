"""Smoke tests for the six studio agents (needs openai-agents, no API key)."""

from __future__ import annotations

import pytest

pytest.importorskip("agents")

from agent.agents import build_llm_manager, build_studio_agents
from agent.brief import EmailBrief


def test_studio_has_six_named_agents():
    studio = build_studio_agents()
    assert studio.manager.name == "Sales Manager"
    assert studio.intake.name == "Intake Checker"
    assert studio.friendly.name == "Friendly Writer"
    assert studio.professional.name == "Professional Writer"
    assert studio.creative.name == "Creative Writer"
    assert studio.picker.name == "Draft Picker"
    assert studio.writers == (studio.friendly, studio.professional, studio.creative)


def test_intake_returns_email_brief_schema():
    studio = build_studio_agents()
    assert studio.intake.output_type is EmailBrief


def test_writers_and_picker_have_intake_guardrail():
    studio = build_studio_agents()
    for agent in (*studio.writers, studio.picker):
        assert agent.input_guardrails
    assert not studio.manager.input_guardrails
    assert not studio.intake.input_guardrails


def test_llm_manager_exposes_three_writer_tools():
    studio = build_studio_agents()
    manager = build_llm_manager(studio.writers)
    assert manager.name == "LLM Sales Manager"
    assert manager.input_guardrails
    names = [getattr(tool, "name", None) for tool in manager.tools]
    assert names == ["friendly_writer", "professional_writer", "creative_writer"]
