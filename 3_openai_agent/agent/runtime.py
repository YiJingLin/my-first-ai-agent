"""Env loading and default model for Sales Email Studio."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

MODEL_NAME = "gpt-4o-mini"


def load_env(*search_roots: Path) -> None:
    """Load .env from each root in order (later files override earlier ones)."""
    for root in search_roots:
        load_dotenv(root / ".env", override=True)
