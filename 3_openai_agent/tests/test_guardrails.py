"""Unit tests for the intake tripwire (no LLM, no Agents SDK)."""

from __future__ import annotations

import pytest

from agent.brief import EmailBrief, with_status
from agent.guardrails import IncompleteBriefError, assert_brief_complete, intake_tripwire


def test_none_brief_trips():
    blocked, missing = intake_tripwire(None)
    assert blocked is True
    assert missing == ["author", "receiver", "field", "purpose"]


def test_partial_brief_trips():
    brief = with_status(EmailBrief(author="Jordan", field="SaaS"))
    blocked, missing = intake_tripwire(brief)
    assert blocked is True
    assert missing == ["receiver", "purpose"]


def test_complete_brief_does_not_trip():
    brief = with_status(
        EmailBrief(
            author="Jordan",
            receiver="Priya",
            field="SaaS analytics",
            purpose="book a demo",
        )
    )
    blocked, missing = intake_tripwire(brief)
    assert blocked is False
    assert missing == []


def test_assert_brief_complete_raises_on_incomplete():
    with pytest.raises(IncompleteBriefError) as exc:
        assert_brief_complete(EmailBrief(author="Jordan"))
    assert "receiver" in exc.value.missing_fields
    assert "field" in exc.value.missing_fields
    assert "purpose" in exc.value.missing_fields


def test_assert_brief_complete_returns_normalized_brief():
    brief = assert_brief_complete(
        EmailBrief(
            author=" Jordan ",
            receiver="Priya",
            field="SaaS",
            purpose="book a demo",
        )
    )
    assert brief.author == "Jordan"
    assert brief.is_complete is True
