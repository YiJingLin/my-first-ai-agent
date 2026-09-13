"""Harness entrypoint: Gradio chat with live policy gate."""

from __future__ import annotations

from pathlib import Path

import gradio as gr

from agent.policy import build_gated_chat
from agent.runtime import load_env

HERE = Path(__file__).resolve().parent
load_env(HERE.parent, HERE)

if __name__ == "__main__":
    gr.ChatInterface(build_gated_chat()).launch(inbrowser=True)
