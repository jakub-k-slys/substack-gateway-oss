from __future__ import annotations

from pydantic import BaseModel

from gateway_pro.converters.markdown import (
    draft_body_to_markdown,
    markdown_to_draft_body,
)
from gateway_pro.models.substack import (
    SubstackDraft,
    SubstackDraftCreated,
    SubstackDraftSummary,
    SubstackUpdateDraftPayload,
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

    @classmethod
    def from_substack(cls, drafts: list[SubstackDraftSummary]) -> DraftsListResponse:
        return cls(items=[DraftSummaryResponse.from_substack(d) for d in drafts])


class CreateDraftRequest(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    body: str | None = None


class UpdateDraftRequest(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    body: str | None = None

    def to_substack_payload(self) -> SubstackUpdateDraftPayload:
        field_map = {
            "title": "draft_title",
            "subtitle": "draft_subtitle",
            "body": "draft_body",
        }
        kwargs: dict[str, str | None] = {}
        for field_name in self.model_fields_set:
            value = getattr(self, field_name)
            if field_name == "body" and value is not None:
                value = markdown_to_draft_body(value)
            kwargs[field_map[field_name]] = value
        return SubstackUpdateDraftPayload(**kwargs)


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
