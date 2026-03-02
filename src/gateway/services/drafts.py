from __future__ import annotations

import logging

from gateway.client.base import SubstackHTTPBase
from gateway.converters.markdown import markdown_to_draft_body
from gateway.models.substack import (
    SubstackDraft,
    SubstackDraftByline,
    SubstackDraftCreated,
    SubstackDraftPayload,
    SubstackDraftSummary,
    SubstackUpdateDraftPayload,
)

_log = logging.getLogger(__name__)


class DraftsMixin(SubstackHTTPBase):
    async def list_drafts(self) -> list[SubstackDraftSummary]:
        """GET /drafts — all drafts as summaries."""
        _log.debug("Listing drafts")
        r = await self._request("GET", f"{self._pub_base}/drafts")
        drafts = [SubstackDraftSummary.model_validate(d) for d in r.json()]
        _log.debug("Got %d drafts", len(drafts))
        return drafts

    async def get_draft(self, draft_id: int) -> SubstackDraft:
        """GET /drafts/{draft_id}."""
        _log.debug("Fetching draft id=%d", draft_id)
        r = await self._request("GET", f"{self._pub_base}/drafts/{draft_id}")
        return SubstackDraft.model_validate(r.json())

    async def update_draft(
        self, draft_id: int, payload: SubstackUpdateDraftPayload
    ) -> SubstackDraft:
        """PUT /drafts/{draft_id} — update only the provided fields."""
        _log.debug("Updating draft id=%d fields=%s", draft_id, payload.model_fields_set)
        r = await self._request(
            "PUT",
            f"{self._pub_base}/drafts/{draft_id}",
            json=payload.model_dump(exclude_unset=True),
        )
        return SubstackDraft.model_validate(r.json())

    async def delete_draft(self, draft_id: int) -> None:
        """DELETE /drafts/{draft_id}."""
        _log.debug("Deleting draft id=%d", draft_id)
        await self._request("DELETE", f"{self._pub_base}/drafts/{draft_id}")
        _log.debug("Deleted draft id=%d", draft_id)

    async def create_draft(
        self,
        title: str | None = None,
        subtitle: str | None = None,
        body: str | None = None,
    ) -> SubstackDraftCreated:
        """POST /drafts — create a new draft, resolving the caller's user ID first."""
        _log.debug("Creating draft title=%r", title)
        user_id = await self._get_own_id()
        payload = SubstackDraftPayload(
            draft_title=title or "",
            draft_subtitle=subtitle or "",
            draft_body=markdown_to_draft_body(body) if body else "",
            draft_bylines=[SubstackDraftByline(id=user_id)],
        )
        r = await self._request(
            "POST", f"{self._pub_base}/drafts", json=payload.model_dump()
        )
        draft = SubstackDraftCreated.model_validate(r.json())
        _log.debug("Created draft id=%d uuid=%s", draft.id, draft.uuid)
        return draft
