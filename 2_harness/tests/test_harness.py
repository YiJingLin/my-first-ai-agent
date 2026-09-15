"""Unit tests for agent.harness — curated cases + offline run (mocked judge)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agent.harness import CASES, run_harness
from agent.policy import REFUSALS


def test_cases_have_unique_ids_and_known_categories():
    ids = [case_id for case_id, _, _ in CASES]
    assert len(ids) == len(set(ids))
    allowed = {"on_topic", *REFUSALS.keys()}
    for case_id, category, message in CASES:
        assert category in allowed, case_id
        assert isinstance(message, str) and message.strip()


def test_run_harness_aggregates_mocked_verdicts():
    fake_client = MagicMock()
    reply_fn = MagicMock(side_effect=["refuse A", "answer B"])
    cases = [
        ("case_a", "unrelated", "Make me a cake"),
        ("case_b", "on_topic", "What skills do you have?"),
    ]

    with patch("agent.harness.judge_reply") as judge:
        judge.side_effect = [
            {"pass": True, "reason": "refused well"},
            {"pass": False, "reason": "went off policy"},
        ]
        rows = run_harness(cases=cases, reply_fn=reply_fn, client=fake_client)

    assert len(rows) == 2
    assert rows[0] == {
        "id": "case_a",
        "category": "unrelated",
        "pass": True,
        "reason": "refused well",
        "reply_preview": "refuse A",
    }
    assert rows[1]["id"] == "case_b"
    assert rows[1]["pass"] is False
    assert rows[1]["reason"] == "went off policy"
    assert reply_fn.call_count == 2
    assert judge.call_count == 2
