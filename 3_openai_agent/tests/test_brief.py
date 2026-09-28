"""Unit tests for EmailBrief merge and completion status."""

from __future__ import annotations

from agent.brief import EmailBrief, compute_missing, merge_briefs, with_status


def test_empty_brief_is_incomplete():
    brief = with_status(EmailBrief())
    assert brief.is_complete is False
    assert brief.missing_fields == ["author", "receiver", "field", "purpose"]


def test_whitespace_slots_count_as_missing():
    brief = with_status(EmailBrief(author="  ", receiver="Priya", field="SaaS", purpose="demo"))
    assert brief.author is None
    assert brief.is_complete is False
    assert brief.missing_fields == ["author"]


def test_complete_brief_has_no_missing_fields():
    brief = with_status(
        EmailBrief(
            author="Jordan",
            receiver="Priya",
            field="SaaS analytics",
            purpose="book a demo",
        )
    )
    assert brief.is_complete is True
    assert brief.missing_fields == []
    assert compute_missing(brief) == []


def test_merge_fills_empty_slots_from_incoming():
    stored = with_status(EmailBrief(author="Jordan"))
    incoming = EmailBrief(receiver="Priya", field="SaaS", purpose="book a demo")

    merged = merge_briefs(stored, incoming)

    assert merged.author == "Jordan"
    assert merged.receiver == "Priya"
    assert merged.field == "SaaS"
    assert merged.purpose == "book a demo"
    assert merged.is_complete is True


def test_merge_does_not_overwrite_with_empty_incoming():
    stored = with_status(EmailBrief(author="Jordan", receiver="Priya"))
    incoming = EmailBrief(author=None, receiver="  ", field="SaaS")

    merged = merge_briefs(stored, incoming)

    assert merged.author == "Jordan"
    assert merged.receiver == "Priya"
    assert merged.field == "SaaS"
    assert merged.is_complete is False
    assert merged.missing_fields == ["purpose"]


def test_merge_overwrites_when_user_corrects_a_slot():
    stored = with_status(EmailBrief(author="Jordan", receiver="Sam"))
    incoming = EmailBrief(receiver="Priya")

    merged = merge_briefs(stored, incoming)

    assert merged.author == "Jordan"
    assert merged.receiver == "Priya"


def test_merge_none_arguments_starts_empty():
    merged = merge_briefs(None, None)
    assert merged.is_complete is False
    assert merged.missing_fields == ["author", "receiver", "field", "purpose"]
