from __future__ import annotations

from pydantic import BaseModel, Field


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


class SubstackScheduledRelease(BaseModel):
    trigger_at: str
    post_audience: str = "only_paid"
    email_audience: str = "only_paid"


class SubstackPrepublish(BaseModel):
    errors: list = Field(default_factory=list)
    suggestions: list = Field(default_factory=list)


class SubstackAiDetection(BaseModel):
    type: str | None = None
    header: str | None = None
    details: str | None = None
    fraction_ai: float | None = None
    fraction_ai_assisted: float | None = None
    fraction_human: float | None = None
    can_disable: bool | None = None
    can_modify_disclosure: bool | None = None
