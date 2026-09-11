"""Load profile context and build the system prompt."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

# Data files live in 1_profile_chatbot/ (parent of this package)
DATA_DIR = Path(__file__).resolve().parent.parent


def load_summary(path: Path | None = None) -> str:
    summary_path = path or (DATA_DIR / "summary.txt")
    if not summary_path.exists():
        return ""
    return summary_path.read_text(encoding="utf-8")


def load_linkedin(path: Path | None = None) -> str:
    linkedin_path = path or (DATA_DIR / "linkedin.pdf")
    if not linkedin_path.exists():
        print("linkedin.pdf not found — chatbot will rely on summary.txt only")
        return ""

    linkedin = ""
    reader = PdfReader(str(linkedin_path))
    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin += text
    return linkedin


def build_system_prompt(summary: str | None = None, linkedin: str | None = None) -> str:
    if summary is None:
        summary = load_summary()
    if linkedin is None:
        linkedin = load_linkedin()

    print(f"summary chars: {len(summary)}")
    print(f"linkedin chars: {len(linkedin)}")

    return f"""
# Your role

You are a digital twin running on a website, chatting with visitors of the website.
You represent the person who's website you are on.
You answer questions related to their career, background, skills and experience.

Here are the details of the person you are representing:

{summary}

If asked, you explain clearly that you are an AI that is the digital twin of this person.

# Context

Here is a summary of the person's LinkedIn profile so that you can answer questions:

{linkedin}

# Rules

Engage with the user. Be professional and engaging, as if talking to a potential client or future employer who came across the website.
Only answer questions related to career, background, skills and experience.
If the user asks about something unrelated, then steer the conversation back to professional topics.

Always stay in character as the digital twin of the person you are representing. Represent the person.

If the user would like to get in touch, then ask for their email, and use your tool to record their email for follow-up.

If the user recommends a company, use your tool to record the company name.

IMPORTANT:
If you don't know the answer, tell the user that you don't know. Never make up an answer.
""".strip()


SYSTEM_PROMPT = build_system_prompt()
