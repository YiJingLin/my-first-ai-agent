"""Unit tests for env loading."""

from __future__ import annotations

import os
from pathlib import Path

from agent.runtime import load_env


def test_load_env_reads_dotenv(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("UNITTEST_SALES_STUDIO_KEY", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("UNITTEST_SALES_STUDIO_KEY=from_dotenv\n", encoding="utf-8")

    load_env(tmp_path)

    assert os.getenv("UNITTEST_SALES_STUDIO_KEY") == "from_dotenv"
