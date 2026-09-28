"""Writer provider and orchestration settings for Sales Email Studio."""

from __future__ import annotations

import os
from typing import Any

from agent.runtime import MODEL_NAME

WRITER_PROVIDERS = ("openai", "google")
ORCHESTRATION_MODES = ("llm", "code")
DEFAULT_WRITER_PROVIDER = "openai"
DEFAULT_ORCHESTRATION = "llm"

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GEMINI_MODEL_NAME = "gemini-2.0-flash"

_gemini_model: Any | None = None


class MissingGoogleApiKeyError(ValueError):
    def __init__(self) -> None:
        super().__init__(
            "Google writers need GOOGLE_API_KEY in the parent .env. "
            "Switch Writer provider back to OpenAI, or add the key and retry."
        )


def normalize_writer_provider(value: str | None) -> str:
    raw = (value or DEFAULT_WRITER_PROVIDER).strip().lower()
    if raw == "openai":
        return "openai"
    if raw in ("google", "gemini"):
        return "google"
    raise ValueError(f"Unknown writer provider: {value!r}")


def normalize_orchestration(value: str | None) -> str:
    raw = (value or DEFAULT_ORCHESTRATION).strip().lower()
    if raw in ("llm", "manager"):
        return "llm"
    if raw in ("code", "gather", "python"):
        return "code"
    raise ValueError(f"Unknown orchestration mode: {value!r}")


def resolve_writer_model(provider: str | None = None) -> Any:
    """OpenAI model id, or a Gemini OpenAIChatCompletionsModel for Google writers."""
    name = normalize_writer_provider(provider)
    if name == "openai":
        return MODEL_NAME
    return _google_writer_model()


def _google_writer_model() -> Any:
    global _gemini_model
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise MissingGoogleApiKeyError()
    if _gemini_model is not None:
        return _gemini_model

    from openai import AsyncOpenAI
    from agents import OpenAIChatCompletionsModel

    client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=api_key)
    _gemini_model = OpenAIChatCompletionsModel(
        model=GEMINI_MODEL_NAME,
        openai_client=client,
    )
    return _gemini_model


def reset_writer_model_cache() -> None:
    """Test helper — drop the cached Gemini client."""
    global _gemini_model
    _gemini_model = None
