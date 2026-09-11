"""Profile chatbot entrypoint: OpenAI tool loop + Gradio UI."""

from __future__ import annotations

import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

from agent.context import SYSTEM_PROMPT
from agent.tools import handle_tool_calls, tools

HERE = Path(__file__).resolve().parent
load_dotenv(HERE.parent / ".env", override=True)
load_dotenv(HERE / ".env", override=True)

MODEL_NAME = "gpt-5.4-mini"
openai = OpenAI()

print("OPENAI_API_KEY:", "ok" if os.getenv("OPENAI_API_KEY") else "missing")


def chat(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
        {"role": "user", "content": message}
    ]
    response = openai.chat.completions.create(
        model=MODEL_NAME, messages=messages, tools=tools
    )
    while response.choices[0].finish_reason == "tool_calls":
        msg = response.choices[0].message
        results = handle_tool_calls(msg.tool_calls)
        messages.append(msg)
        messages.extend(results)
        response = openai.chat.completions.create(
            model=MODEL_NAME, messages=messages, tools=tools
        )
    return response.choices[0].message.content


if __name__ == "__main__":
    gr.ChatInterface(chat).launch(inbrowser=True)
