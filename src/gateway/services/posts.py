from __future__ import annotations

import logging

from gateway.client.base import SubstackHTTPBase
from gateway.models.substack import (
    SubstackComment,
    SubstackCommentsResponse,
    SubstackFullPost,
    SubstackNotesPage,
    SubstackPostResponse,
    SubstackProfilePostsPage,
)

_log = logging.getLogger(__name__)


class PostsService:
    def __init__(self, client: SubstackHTTPBase) -> None:
        self._client = client

    async def get_posts_for_profile(
        self, profile_id: int, limit: int = 25, offset: int = 0
    ) -> SubstackProfilePostsPage:
        """GET /profile/posts — posts for a given profile ID."""
        _log.debug(
            "Fetching posts for profile_id=%d (limit=%d, offset=%d)",
            profile_id,
            limit,
            offset,
        )
        params = {"profile_user_id": profile_id, "limit": limit, "offset": offset}
        r = await self._client._request(
            "GET", f"{self._client._sub_base}/profile/posts", params=params
        )
        page = SubstackProfilePostsPage.model_validate(r.json())
        _log.debug(
            "Got %d posts for profile_id=%d (next_cursor=%r)",
            len(page.posts),
            profile_id,
            page.next_cursor,
        )
        return page

    async def get_notes_for_profile(
        self, profile_id: int, cursor: str | None = None
    ) -> SubstackNotesPage:
        """GET /reader/feed/profile/{id}?types=note — notes for a given profile ID."""
        _log.debug("Fetching notes for profile_id=%d (cursor=%r)", profile_id, cursor)
        params: dict[str, str] = {"types": "note"}
        if cursor:
            params["cursor"] = cursor
        r = await self._client._request(
            "GET",
            f"{self._client._pub_base}/reader/feed/profile/{profile_id}",
            params=params,
        )
        page = SubstackNotesPage.model_validate(r.json())
        _log.debug(
            "Got %d notes for profile_id=%d (next_cursor=%r)",
            len(page.items),
            profile_id,
            page.next_cursor,
        )
        return page

    async def get_post_by_id(self, post_id: int) -> SubstackFullPost:
        """GET /posts/by-id/{id} — full post by numeric ID."""
        _log.debug("Fetching post id=%d", post_id)
        r = await self._client._request(
            "GET", f"{self._client._sub_base}/posts/by-id/{post_id}"
        )
        return SubstackPostResponse.model_validate(r.json()).post

    async def get_comments_for_post(self, post_id: int) -> list[SubstackComment]:
        """GET /post/{id}/comments — all comments for a post."""
        _log.debug("Fetching comments for post id=%d", post_id)
        r = await self._client._request(
            "GET", f"{self._client._pub_base}/post/{post_id}/comments"
        )
        comments = SubstackCommentsResponse.model_validate(r.json()).comments
        _log.debug("Got %d comments for post id=%d", len(comments), post_id)
        return comments
