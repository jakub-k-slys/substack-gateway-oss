from __future__ import annotations

import asyncio
from typing import Literal
from urllib.parse import urlencode

from gateway_oss.services.following import FollowingService

from gateway_pro.services.profile_feed import (
    AtomFeedAuthor,
    AtomFeedEntry,
    AtomFeedPage,
    ProfileFeedService,
)


class FollowingFeedService:
    def __init__(
        self, following: FollowingService, profile_feed: ProfileFeedService
    ) -> None:
        self._following = following
        self._profile_feed = profile_feed

    async def get_feed_page(
        self,
        *,
        feed_type: Literal["mixed", "post", "note"] = "mixed",
        limit: int = 10,
        total: int | None = None,
        feed_url: str,
    ) -> AtomFeedPage:
        following = await self._following.get_own_following()
        entries_by_author = await asyncio.gather(
            *[
                self._profile_feed.get_entries_for_profile(
                    user.id,
                    fallback_author=AtomFeedAuthor(
                        name=user.handle,
                        handle=user.handle,
                        avatar_url="",
                    ),
                    feed_type=feed_type,
                    limit=limit,
                )
                for user in following
            ]
        )
        entries: list[AtomFeedEntry] = []
        for page in entries_by_author:
            entries.extend(page.entries)
        entries.sort(key=lambda entry: entry.updated_at, reverse=True)
        if total is not None:
            entries = entries[:total]
        updated_at = entries[0].updated_at if entries else "1970-01-01T00:00:00Z"
        author = AtomFeedAuthor(
            name="Following feed",
            handle="me",
            avatar_url="",
        )
        return AtomFeedPage(
            feed_id="tag:substack-gateway,following",
            title="Following on Substack",
            subtitle="Recent posts and notes from the people you follow",
            author=author,
            updated_at=updated_at,
            icon_url=None,
            alternate_url="https://substack.com/feed/following",
            self_url=self._build_feed_url(
                feed_url,
                feed_type=feed_type,
                limit=limit,
                total=total,
            ),
            next_url=None,
            entries=entries,
        )

    def _build_feed_url(
        self,
        feed_url: str,
        *,
        feed_type: Literal["mixed", "post", "note"],
        limit: int,
        total: int | None,
    ) -> str:
        query_params = {
            "limit": str(limit),
            "type": feed_type,
        }
        if total is not None:
            query_params["total"] = str(total)
        query = urlencode(query_params)
        return f"{feed_url}?{query}"
