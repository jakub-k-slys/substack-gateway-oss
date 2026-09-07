from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from gateway_drafts.converters.markdown import draft_body_to_markdown
from gateway_drafts.models.substack import (
    SubstackAiDetection,
    SubstackDraft,
    SubstackDraftCreated,
    SubstackDraftSummary,
    SubstackPrepublish,
    SubstackScheduledRelease,
)


class DraftSummaryResponse(BaseModel):
    id: int
    uuid: str
    title: str | None = None
    updated: str | None = None

    @classmethod
    def from_substack(cls, draft: SubstackDraftSummary) -> DraftSummaryResponse:
        return cls(
            id=draft.id,
            uuid=draft.uuid,
            title=draft.draft_title,
            updated=draft.draft_updated_at,
        )


class DraftsListResponse(BaseModel):
    items: list[DraftSummaryResponse]
    next: str | None = None

    @classmethod
    def from_substack(
        cls,
        drafts: list[SubstackDraftSummary],
        next_cursor: str | None = None,
    ) -> DraftsListResponse:
        return cls(
            items=[DraftSummaryResponse.from_substack(d) for d in drafts],
            next=next_cursor,
        )


class CreateDraftRequest(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    body: str | None = None


class UpdateDraftRequest(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    body: str | None = None

    def provided_updates(self) -> dict[str, str | None]:
        """The subset of {title, subtitle, body} the caller actually set."""
        return {name: getattr(self, name) for name in self.model_fields_set}


class CreateDraftResponse(BaseModel):
    id: int
    uuid: str

    @classmethod
    def from_substack(cls, draft: SubstackDraftCreated) -> CreateDraftResponse:
        return cls(id=draft.id, uuid=draft.uuid)


class DraftResponse(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    body: str | None = None

    @classmethod
    def from_substack(cls, draft: SubstackDraft) -> DraftResponse:
        return cls(
            title=draft.draft_title,
            subtitle=draft.draft_subtitle,
            body=draft_body_to_markdown(draft.draft_body) if draft.draft_body else None,
        )


class ScheduleDraftRequest(BaseModel):
    scheduled_at: datetime
    post_audience: str | None = None
    email_audience: str | None = None


class ScheduleDraftResponse(BaseModel):
    scheduled_at: str
    post_audience: str
    email_audience: str

    @classmethod
    def from_substack(cls, release: SubstackScheduledRelease) -> ScheduleDraftResponse:
        return cls(
            scheduled_at=release.trigger_at,
            post_audience=release.post_audience,
            email_audience=release.email_audience,
        )


class PrepublishResponse(BaseModel):
    errors: list = Field(default_factory=list)
    suggestions: list = Field(default_factory=list)

    @classmethod
    def from_substack(cls, data: SubstackPrepublish) -> PrepublishResponse:
        return cls(errors=data.errors, suggestions=data.suggestions)


class AiDetectionResponse(BaseModel):
    type: str | None = None
    header: str | None = None
    details: str | None = None
    fraction_ai: float | None = None
    fraction_ai_assisted: float | None = None
    fraction_human: float | None = None
    can_disable: bool | None = None
    can_modify_disclosure: bool | None = None

    @classmethod
    def from_substack(cls, d: SubstackAiDetection) -> AiDetectionResponse:
        return cls(
            type=d.type,
            header=d.header,
            details=d.details,
            fraction_ai=d.fraction_ai,
            fraction_ai_assisted=d.fraction_ai_assisted,
            fraction_human=d.fraction_human,
            can_disable=d.can_disable,
            can_modify_disclosure=d.can_modify_disclosure,
        )


class ImageUploadResult(BaseModel):
    id: int
    url: str
    width: int
    height: int
    bytes: int
    content_type: str

    @classmethod
    def from_substack(cls, data: dict) -> ImageUploadResult:
        return cls(
            id=data["id"],
            url=data["url"],
            width=data["imageWidth"],
            height=data["imageHeight"],
            bytes=data["bytes"],
            content_type=data["contentType"],
        )
