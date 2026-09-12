"""Shared OpenAI + tool chat loop used by local and Spaces entrypoints."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

from dotenv import load_dotenv
from openai import OpenAI

from agent.context import SYSTEM_PROMPT
from agent.tools import handle_tool_calls, tools

MODEL_NAME = "gpt-5.4-mini"


def load_env(*search_roots: Path) -> None:
    """Load .env from each root in order (later files override earlier ones)."""
    for root in search_roots:
        load_dotenv(root / ".env", override=True)


def build_chat(model: str = MODEL_NAME) -> Callable:
    client = OpenAI()
    print("OPENAI_API_KEY:", "ok" if os.getenv("OPENAI_API_KEY") else "missing")

    def chat(message, history):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
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

    return chat
