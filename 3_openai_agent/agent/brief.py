"""Sales-email brief: required slots and merge across chat turns."""

from __future__ import annotations

from pydantic import BaseModel, Field

REQUIRED_FIELDS = ("author", "receiver", "field", "purpose")


class EmailBrief(BaseModel):
    author: str | None = None
    receiver: str | None = None
    field: str | None = None
    purpose: str | None = None
    missing_fields: list[str] = Field(default_factory=list)
    is_complete: bool = False


def normalize_slot(value: str | None) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def compute_missing(brief: EmailBrief) -> list[str]:
    return [
        name
        for name in REQUIRED_FIELDS
        if normalize_slot(getattr(brief, name, None)) is None
    ]


def with_status(brief: EmailBrief) -> EmailBrief:
    """Recompute missing_fields / is_complete from the four required slots."""
    missing = compute_missing(brief)
    return brief.model_copy(
        update={
            "author": normalize_slot(brief.author),
            "receiver": normalize_slot(brief.receiver),
            "field": normalize_slot(brief.field),
            "purpose": normalize_slot(brief.purpose),
            "missing_fields": missing,
            "is_complete": not missing,
        }
    )


def merge_briefs(stored: EmailBrief | None, incoming: EmailBrief | None) -> EmailBrief:
    """Keep stored slots; overwrite a slot only when incoming has a new value."""
    stored = stored or EmailBrief()
    incoming = incoming or EmailBrief()
    data: dict[str, str | None] = {}
    for name in REQUIRED_FIELDS:
        new = normalize_slot(getattr(incoming, name, None))
        old = normalize_slot(getattr(stored, name, None))
        data[name] = new if new is not None else old
    return with_status(EmailBrief(**data))
