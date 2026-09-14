"""Unit tests for agent.context — file load and prompt assembly (no OpenAI)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from agent.context import build_system_prompt, load_linkedin, load_summary


def test_load_summary_missing(tmp_path: Path):
    assert load_summary(tmp_path / "missing.txt") == ""


def test_load_summary_reads_file(tmp_path: Path):
    path = tmp_path / "summary.txt"
    path.write_text("Jordan builds agents", encoding="utf-8")
    assert load_summary(path) == "Jordan builds agents"


def test_load_linkedin_missing(tmp_path: Path):
    assert load_linkedin(tmp_path / "missing.pdf") == ""


def test_load_linkedin_extracts_text(tmp_path: Path):
    path = tmp_path / "linkedin.pdf"
    path.write_bytes(b"%PDF-fake")  # existence only; PdfReader is mocked

    page = MagicMock()
    page.extract_text.return_value = "Experience at Acme"
    reader = MagicMock()
    reader.pages = [page]

    with patch("agent.context.PdfReader", return_value=reader) as pdf_reader:
        text = load_linkedin(path)

    pdf_reader.assert_called_once_with(str(path))
    assert text == "Experience at Acme"


def test_build_system_prompt_injects_summary_and_linkedin():
    prompt = build_system_prompt(summary="SUM_MARKER", linkedin="LI_MARKER")
    assert "SUM_MARKER" in prompt
    assert "LI_MARKER" in prompt
    assert "digital twin" in prompt.lower()
    assert "record their email" in prompt.lower()
