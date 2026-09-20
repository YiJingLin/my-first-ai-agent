"""Unit tests for agent.tools — dispatch and return shape (no OpenAI)."""

from __future__ import annotations

import json
from types import SimpleNamespace

from agent.tools import (
    handle_tool_calls,
    record_recommended_company,
    record_user_details,
    tools,
)


def _tool_call(name: str, args_json: str, call_id: str = "call_1"):
    return SimpleNamespace(
        id=call_id,
        function=SimpleNamespace(name=name, arguments=args_json),
    )


def test_record_user_details_returns_ok():
    assert record_user_details("a@b.com") == "OK"


def test_record_user_details_defaults():
    assert record_user_details("a@b.com", name="Jordan") == "OK"


def test_record_recommended_company_returns_ok():
    assert record_recommended_company("Acme") == "OK"


def test_handle_known_tool_record_user_details():
    results = handle_tool_calls(
        [_tool_call("record_user_details", '{"email": "a@b.com"}')]
    )
    assert len(results) == 1
    assert results[0]["role"] == "tool"
    assert results[0]["tool_call_id"] == "call_1"
    assert json.loads(results[0]["content"]) == "OK"


def test_handle_known_tool_record_recommended_company():
    results = handle_tool_calls(
        [_tool_call("record_recommended_company", '{"company_name": "Acme"}', "call_2")]
    )
    assert results[0]["tool_call_id"] == "call_2"
    assert json.loads(results[0]["content"]) == "OK"


def test_handle_unknown_tool():
    results = handle_tool_calls([_tool_call("nope", "{}")])
    assert json.loads(results[0]["content"]) == "Unknown tool: nope"


def test_handle_multiple_tool_calls():
    results = handle_tool_calls(
        [
            _tool_call("record_user_details", '{"email": "a@b.com"}', "c1"),
            _tool_call("record_recommended_company", '{"company_name": "Acme"}', "c2"),
        ]
    )
    assert len(results) == 2
    assert [r["tool_call_id"] for r in results] == ["c1", "c2"]


def test_tools_schemas_have_required_keys():
    assert len(tools) == 2
    for entry in tools:
        assert entry["type"] == "function"
        fn = entry["function"]
        assert "name" in fn
        assert "parameters" in fn
        assert "required" in fn["parameters"]
