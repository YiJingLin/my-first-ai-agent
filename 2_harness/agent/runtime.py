"""OpenAI tool chat loop for the raw career twin (no policy gate)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

from dotenv import load_dotenv
from openai import OpenAI

from agent.context import SYSTEM_PROMPT
from agent.tools import handle_tool_calls, tools

MODEL_NAME = "gpt-5.4-mini"
JUDGE_MODEL = MODEL_NAME


def load_env(*search_roots: Path) -> None:
    """Load .env from each root in order (later files override earlier ones)."""
    for root in search_roots:
        load_dotenv(root / ".env", override=True)


def build_generate_reply(
    client: OpenAI | None = None,
    model: str = MODEL_NAME,
    system_prompt: str = SYSTEM_PROMPT,
) -> Callable:
    """Raw twin reply — no policy gate."""
    client = client or OpenAI()
    print("OPENAI_API_KEY:", "ok" if os.getenv("OPENAI_API_KEY") else "missing")

    def generate_reply(message, history):
        messages = [{"role": "system", "content": system_prompt}] + history + [
            {"role": "user", "content": message}
        ]
        response = client.chat.completions.create(
            model=model, messages=messages, tools=tools
        )
        while response.choices[0].finish_reason == "tool_calls":
            msg = response.choices[0].message
            results = handle_tool_calls(msg.tool_calls)
            messages.append(msg)
            messages.extend(results)
            response = client.chat.completions.create(
                model=model, messages=messages, tools=tools
            )
        return response.choices[0].message.content

    return generate_reply
