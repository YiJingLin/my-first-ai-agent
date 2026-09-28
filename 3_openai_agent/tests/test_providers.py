"""Unit tests for writer provider and orchestration settings."""

from __future__ import annotations

import pytest

from agent.providers import (
    GEMINI_MODEL_NAME,
    MissingGoogleApiKeyError,
    normalize_orchestration,
    normalize_writer_provider,
    reset_writer_model_cache,
    resolve_writer_model,
)
from agent.runtime import MODEL_NAME


def test_normalize_writer_provider_aliases():
    assert normalize_writer_provider("OpenAI") == "openai"
    assert normalize_writer_provider("Gemini") == "google"
    assert normalize_writer_provider(None) == "openai"


def test_normalize_orchestration_aliases():
    assert normalize_orchestration("LLM") == "llm"
    assert normalize_orchestration("Code") == "code"
    assert normalize_orchestration(None) == "llm"


def test_unknown_settings_raise():
    with pytest.raises(ValueError, match="writer provider"):
        normalize_writer_provider("anthropic")
    with pytest.raises(ValueError, match="orchestration"):
        normalize_orchestration("handoff")


def test_openai_writer_model_is_default_id():
    assert resolve_writer_model("openai") == MODEL_NAME


def test_google_writer_model_requires_api_key(monkeypatch):
    reset_writer_model_cache()
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    with pytest.raises(MissingGoogleApiKeyError, match="GOOGLE_API_KEY"):
        resolve_writer_model("google")


def test_google_writer_model_uses_gemini(monkeypatch):
    pytest.importorskip("agents")
    reset_writer_model_cache()
    monkeypatch.setenv("GOOGLE_API_KEY", "test-google-key")
    model = resolve_writer_model("Google")
    assert getattr(model, "model", None) == GEMINI_MODEL_NAME
    reset_writer_model_cache()
