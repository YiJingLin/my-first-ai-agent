"""Hugging Face Spaces entrypoint (keep this file named app.py)."""

from __future__ import annotations

from pathlib import Path

import gradio as gr

from agent.runtime import build_chat, load_env

HERE = Path(__file__).resolve().parent
# Local smoke-test: parent project .env; on Spaces, secrets are already in the env
load_env(HERE.parent.parent, HERE.parent, HERE)

if __name__ == "__main__":
    gr.ChatInterface(build_chat()).launch()
