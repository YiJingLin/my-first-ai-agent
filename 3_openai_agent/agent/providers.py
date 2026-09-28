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
# Default Google writer model. Change here (or set GEMINI_MODEL in parent .env).
# gemini-2.0-flash: shut down 2026-06-01.
# gemini-2.5-flash / gemini-2.5-flash-lite: often blocked for *new* API users
# ("no longer available to new users"). Prefer 3.x for new keys:
#   gemini-3.8-flash (docs default) or gemini-3.5-flash-lite (cheaper).
GEMINI_MODEL_NAME = "gemini-3.8-flash"

_gemini_model: Any | None = None


class MissingApiKeyError(ValueError):
    """Raised when a required API key is missing or whitespace-only."""


class MissingOpenAIApiKeyError(MissingApiKeyError):
    def __init__(self) -> None:
        super().__init__(
            "OPENAI_API_KEY is missing from the parent .env. "
            "Intake, the Sales Manager, and the picker need it even when writers use Google."
        )


class MissingGoogleApiKeyError(MissingApiKeyError):
    def __init__(self) -> None:
        super().__init__(
            "Google writers need GOOGLE_API_KEY in the parent .env. "
            "Switch Writer provider back to OpenAI, or add the key and retry."
        )


def require_api_key(env_name: str) -> str:
    """Return the stripped key, or raise if unset / whitespace-only."""
    value = (os.getenv(env_name) or "").strip()
    if not value:
        if env_name == "GOOGLE_API_KEY":
            raise MissingGoogleApiKeyError()
        if env_name == "OPENAI_API_KEY":
            raise MissingOpenAIApiKeyError()
        raise MissingApiKeyError(f"{env_name} is missing.")
    return value


def require_openai_api_key() -> str:
    return require_api_key("OPENAI_API_KEY")


def require_google_api_key() -> str:
    return require_api_key("GOOGLE_API_KEY")


def gemini_model_name() -> str:
    configured = (os.getenv("GEMINI_MODEL") or GEMINI_MODEL_NAME).strip()
    return configured or GEMINI_MODEL_NAME


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
        require_openai_api_key()
        return MODEL_NAME
    return _google_writer_model()


def _google_writer_model() -> Any:
    global _gemini_model
    api_key = require_google_api_key()
    if _gemini_model is not None:
        return _gemini_model

    from openai import AsyncOpenAI
    from agents import OpenAIChatCompletionsModel

    client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=api_key)
    _gemini_model = OpenAIChatCompletionsModel(
        model=gemini_model_name(),
        openai_client=client,
    )
    return _gemini_model


def reset_writer_model_cache() -> None:
    """Test helper — drop the cached Gemini client."""
    global _gemini_model
    _gemini_model = None
