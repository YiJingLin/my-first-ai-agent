"""Gradio entrypoint: Sales Manager chat with intake gate + draft settings."""

from __future__ import annotations

from pathlib import Path

import gradio as gr

from agent.orchestrate import build_chat
from agent.runtime import load_env

HERE = Path(__file__).resolve().parent
load_env(HERE.parent, HERE)

if __name__ == "__main__":
    gr.ChatInterface(
        build_chat(),
        title="Sales Email Studio",
        description=(
            "I help you construct a sales email. "
            "I'll collect author, receiver, field/domain, and purpose first, "
            "then draft three styles and pick the best one. "
            "Use Settings to switch writer provider (OpenAI / Google) "
            "and orchestration (LLM manager / code gather)."
        ),
        additional_inputs=[
            gr.Radio(
                ["OpenAI", "Google"],
                value="OpenAI",
                label="Writer provider",
            ),
            gr.Radio(
                ["LLM", "Code"],
                value="LLM",
                label="Orchestration",
            ),
        ],
        additional_inputs_accordion="Settings",
    ).launch(inbrowser=True)
