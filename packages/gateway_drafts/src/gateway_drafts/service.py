from __future__ import annotations

import json
import logging
from datetime import UTC, datetime

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_drafts._cursor import decode_offset, encode_offset
from gateway_drafts.converters.draft_body_resolver import resolve_draft_body
from gateway_drafts.converters.markdown import markdown_to_draft_doc
from gateway_drafts.models.substack import (
    SubstackAiDetection,
    SubstackDraft,
    SubstackDraftByline,
    SubstackDraftCreated,
    SubstackDraftPayload,
    SubstackDraftSummary,
    SubstackPrepublish,
    SubstackScheduledRelease,
    SubstackUpdateDraftPayload,
)

_log = logging.getLogger(__name__)


def to_trigger_at(value: str | datetime) -> str:
    """Normalize a datetime or ISO-8601 string to Substack's UTC trigger format."""
    dt = (
        value
        if isinstance(value, datetime)
        else datetime.fromisoformat(value.replace("Z", "+00:00"))
    )
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.000Z")


_UPDATE_FIELD_MAP = {
    "title": "draft_title",
    "subtitle": "draft_subtitle",
    "body": "draft_body",
}


class DraftsService:
    def __init__(self, pub: PublicationClient, sub: SubstackClient) -> None:
        self._pub = pub
        self._sub = sub

    async def _build_body(self, markdown: str) -> str:
        doc = markdown_to_draft_doc(markdown)
        doc = await resolve_draft_body(doc, self._pub)
        return json.dumps(doc, ensure_ascii=False)

    async def list_drafts(
        self,
        cursor: str | None = None,
        limit: int = 10,
    ) -> tuple[list[SubstackDraftSummary], str | None]:
        """GET /post_management/drafts — cursor-paginated drafts, newest first.

        Returns (items, next_cursor). `next_cursor` is None when no further
        pages remain.
        """
        offset = decode_offset(cursor) if cursor else 0
        _log.debug("Listing drafts offset=%d limit=%d", offset, limit)
        r = await self._pub.get(
            "post_management/drafts",
            params={
                "offset": offset,
                "limit": limit,
                "order_by": "draft_updated_at",
                "order_direction": "desc",
            },
        )
        data = r.json()
        raw_items = data.get("posts", []) if isinstance(data, dict) else data
        drafts = [SubstackDraftSummary.model_validate(d) for d in raw_items]
        total = data.get("total") if isinstance(data, dict) else None
        consumed = offset + len(drafts)
        has_more = len(drafts) == limit and (total is None or consumed < total)
        next_cursor = encode_offset(consumed) if has_more else None
        _log.debug("Got %d drafts (next=%s)", len(drafts), next_cursor)
        return drafts, next_cursor

    async def get_draft(self, draft_id: int) -> SubstackDraft:
        """GET /drafts/{draft_id}."""
        _log.debug("Fetching draft id=%d", draft_id)
        r = await self._pub.get(f"drafts/{draft_id}")
        return SubstackDraft.model_validate(r.json())

    async def update_draft(
        self, draft_id: int, updates: dict[str, str | None]
    ) -> SubstackDraft:
        """PUT /drafts/{draft_id} — update only the provided fields."""
        _log.debug("Updating draft id=%d fields=%s", draft_id, list(updates))
        payload_kwargs: dict[str, str | None] = {}
        for name, value in updates.items():
            if name == "body" and value is not None:
                value = await self._build_body(value)
            payload_kwargs[_UPDATE_FIELD_MAP[name]] = value
        payload = SubstackUpdateDraftPayload(**payload_kwargs)
        r = await self._pub.put(
            f"drafts/{draft_id}",
            json=payload.model_dump(exclude_unset=True),
        )
        return SubstackDraft.model_validate(r.json())

    async def delete_draft(self, draft_id: int) -> None:
        """DELETE /drafts/{draft_id}."""
        _log.debug("Deleting draft id=%d", draft_id)
        await self._pub.delete(f"drafts/{draft_id}")
        _log.debug("Deleted draft id=%d", draft_id)

    async def create_draft(
        self,
        title: str | None = None,
        subtitle: str | None = None,
        body: str | None = None,
    ) -> SubstackDraftCreated:
        """POST /drafts — create a new draft, resolving the caller's user ID first."""
        _log.debug("Creating draft title=%r", title)
        user_id = await self._sub.get_own_id()
        payload = SubstackDraftPayload(
            draft_title=title or "",
            draft_subtitle=subtitle or "",
            draft_body=(await self._build_body(body)) if body else "",
            draft_bylines=[SubstackDraftByline(id=user_id)],
        )
        r = await self._pub.post("drafts", json=payload.model_dump())
        draft = SubstackDraftCreated.model_validate(r.json())
        _log.debug("Created draft id=%d uuid=%s", draft.id, draft.uuid)
        return draft

    async def ai_detection(self, draft_id: int) -> SubstackAiDetection:
        """GET /drafts/{draft_id}/pangram_detection — Pangram AI-writing scan."""
        _log.debug("AI detection draft id=%d", draft_id)
        r = await self._pub.get(f"drafts/{draft_id}/pangram_detection")
        return SubstackAiDetection.model_validate(r.json())

    async def prepublish_draft(self, draft_id: int) -> SubstackPrepublish:
        """GET /drafts/{draft_id}/prepublish — editor pre-publish validation."""
        _log.debug("Prepublish check draft id=%d", draft_id)
        r = await self._pub.get(f"drafts/{draft_id}/prepublish")
        return SubstackPrepublish.model_validate(r.json())

    async def schedule_draft(
        self,
        draft_id: int,
        scheduled_at: str | datetime,
        post_audience: str = "only_paid",
        email_audience: str = "only_paid",
    ) -> SubstackScheduledRelease:
        """POST /drafts/{draft_id}/scheduled_release — schedule timed release."""
        release = SubstackScheduledRelease(
            trigger_at=to_trigger_at(scheduled_at),
            post_audience=post_audience,
            email_audience=email_audience,
        )
        _log.debug("Scheduling draft id=%d at=%s", draft_id, release.trigger_at)
        await self._pub.post(
            f"drafts/{draft_id}/scheduled_release",
            json=release.model_dump(),
        )
        return release

    async def unschedule_draft(self, draft_id: int) -> None:
        """DELETE /drafts/{draft_id}/scheduled_release — cancel scheduled release."""
        _log.debug("Unscheduling draft id=%d", draft_id)
        await self._pub.delete(f"drafts/{draft_id}/scheduled_release")
