from __future__ import annotations

from pydantic import BaseModel


class SubstackDraftByline(BaseModel):
    id: int
    is_guest: bool = False


class SubstackDraftPayload(BaseModel):
    draft_title: str = ""
    draft_subtitle: str = ""
    draft_podcast_url: str | None = None
    draft_podcast_duration: str | None = None
    draft_body: str = ""
    section_chosen: bool = False
    draft_section_id: int | None = None
    draft_bylines: list[SubstackDraftByline]
    audience: str = "only_paid"
    type: str = "newsletter"


class SubstackDraftCreated(BaseModel):
    id: int
    uuid: str


class SubstackDraftSummary(BaseModel):
    id: int
    uuid: str
    draft_title: str | None = None
    draft_updated_at: str | None = None


class SubstackDraft(BaseModel):
    draft_title: str | None = None
    draft_subtitle: str | None = None
    draft_body: str | None = None


class SubstackUpdateDraftPayload(BaseModel):
    draft_title: str | None = None
    draft_subtitle: str | None = None
    draft_body: str | None = None
