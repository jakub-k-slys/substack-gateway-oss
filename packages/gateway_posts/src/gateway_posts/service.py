from __future__ import annotations

import logging

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_core.models.substack import (
    SubstackFullPost,
    SubstackPostResponse,
    SubstackProfilePostsPage,
)

_log = logging.getLogger(__name__)


class PostsService:
    def __init__(self, pub: PublicationClient, sub: SubstackClient) -> None:
        self._pub = pub
        self._sub = sub

    async def get_posts_for_profile(
        self,
        profile_id: int,
        limit: int = 25,
        cursor: str | None = None,
    ) -> SubstackProfilePostsPage:
        """GET /profile/posts — posts for a given profile ID."""
        _log.debug(
            "Fetching posts for profile_id=%d (limit=%d, cursor=%r)",
            profile_id,
            limit,
            cursor,
        )
        params: dict[str, str | int] = {
            "profile_user_id": profile_id,
            "limit": limit,
        }
        if cursor:
            params["cursor"] = cursor
        r = await self._sub.get("profile/posts", params=params)
        page = SubstackProfilePostsPage.model_validate(r.json())
        _log.debug(
            "Got %d posts for profile_id=%d (next_cursor=%r)",
            len(page.posts),
            profile_id,
            page.next_cursor,
        )
        return page

    async def get_post_by_id(self, post_id: int) -> SubstackFullPost:
        """GET /posts/by-id/{id} — full post by numeric ID."""
        _log.debug("Fetching post id=%d", post_id)
        r = await self._sub.get(f"posts/by-id/{post_id}")
        return SubstackPostResponse.model_validate(r.json()).post
