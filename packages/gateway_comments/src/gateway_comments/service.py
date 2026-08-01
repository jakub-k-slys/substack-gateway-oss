from __future__ import annotations

import logging

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_core.models.substack import (
    SubstackComment,
    SubstackCommentsResponse,
    SubstackItemResponse,
    SubstackNote,
)

_log = logging.getLogger(__name__)


class CommentsService:
    def __init__(self, pub: PublicationClient, sub: SubstackClient) -> None:
        self._pub = pub
        self._sub = sub

    async def get_comments_for_post(self, post_id: int) -> list[SubstackComment]:
        """GET /post/{id}/comments — all comments for a post."""
        r = await self._pub.get(f"post/{post_id}/comments")
        return SubstackCommentsResponse.model_validate(r.json()).comments

    async def get_comment_by_id(self, comment_id: int) -> SubstackNote:
        """GET /reader/comment/{id} — a single comment in the reader wire format."""
        r = await self._pub.get(f"reader/comment/{comment_id}")
        return SubstackItemResponse.model_validate(r.json()).item
