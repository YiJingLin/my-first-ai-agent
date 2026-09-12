"""Profile chatbot entrypoint: OpenAI tool loop + Gradio UI."""

from __future__ import annotations

from pathlib import Path

import gradio as gr

from agent.runtime import build_chat, load_env

HERE = Path(__file__).resolve().parent
load_env(HERE.parent, HERE)

if __name__ == "__main__":
    gr.ChatInterface(build_chat()).launch(inbrowser=True)
