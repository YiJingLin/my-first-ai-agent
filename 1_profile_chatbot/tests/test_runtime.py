"""Unit tests for agent.runtime — chat loop with mocked OpenAI client."""

from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from agent.runtime import build_chat, load_env


def _tool_call(name: str, args_json: str, call_id: str = "call_1"):
    return SimpleNamespace(
        id=call_id,
        function=SimpleNamespace(name=name, arguments=args_json),
    )


def test_load_env_reads_dotenv(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("UNITTEST_PROFILE_CHATBOT_KEY", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("UNITTEST_PROFILE_CHATBOT_KEY=from_dotenv\n", encoding="utf-8")

    load_env(tmp_path)

    assert os.getenv("UNITTEST_PROFILE_CHATBOT_KEY") == "from_dotenv"


def test_chat_returns_content_without_tools():
    fake_response = MagicMock()
    fake_response.choices = [
        MagicMock(finish_reason="stop", message=MagicMock(content="Hello"))
    ]
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value = fake_response

    with patch("agent.runtime.OpenAI", return_value=fake_client):
        chat = build_chat(model="test-model")
        assert chat("hi", []) == "Hello"

    create = fake_client.chat.completions.create
    assert create.call_count == 1
    kwargs = create.call_args.kwargs
    assert kwargs["model"] == "test-model"
    assert kwargs["messages"][0]["role"] == "system"
    assert kwargs["messages"][-1] == {"role": "user", "content": "hi"}


def test_chat_runs_tool_loop_then_answers():
    tool_msg = MagicMock()
    tool_msg.tool_calls = [
        _tool_call("record_user_details", '{"email": "a@b.com"}'),
    ]
    first = MagicMock(choices=[MagicMock(finish_reason="tool_calls", message=tool_msg)])
    second = MagicMock(
        choices=[MagicMock(finish_reason="stop", message=MagicMock(content="Done"))]
    )
    fake_client = MagicMock()
    fake_client.chat.completions.create.side_effect = [first, second]

    with patch("agent.runtime.OpenAI", return_value=fake_client):
        chat = build_chat()
        assert chat("email me at a@b.com", []) == "Done"

    assert fake_client.chat.completions.create.call_count == 2
    second_messages = fake_client.chat.completions.create.call_args_list[1].kwargs[
        "messages"
    ]
    tool_results = [m for m in second_messages if isinstance(m, dict) and m.get("role") == "tool"]
    assert len(tool_results) == 1
    assert tool_results[0]["tool_call_id"] == "call_1"
