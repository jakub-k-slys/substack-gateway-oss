from __future__ import annotations

import asyncio
from typing import Literal
from urllib.parse import urlencode

from aiocache import SimpleMemoryCache, cached_stampede
from gateway_oss.config import settings
from gateway_oss.models.substack import SubstackFollowingUser
from gateway_oss.services.following import FollowingService

from gateway_pro.services.profile_feed import (
    AtomFeedAuthor,
    AtomFeedEntriesPage,
    AtomFeedEntry,
    AtomFeedPage,
    ProfileFeedService,
)


def _build_followed_profile_feed_cache_key(
    func, _self, user: SubstackFollowingUser, *, feed_type: str, limit: int
) -> str:
    return ":".join(
        (
            func.__module__,
            func.__qualname__,
            str(user.id),
            feed_type,
            str(limit),
        )
    )


_followed_profile_feed_cache = cached_stampede(
    cache=SimpleMemoryCache,
    ttl=settings.following_feed_profile_cache_ttl_sec,
    lease=2,
    key_builder=_build_followed_profile_feed_cache_key,
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
                self._get_followed_profile_entries(
                    user,
                    feed_type=feed_type,
                    limit=limit,
                )
                for user in following
            ]
        )
        entries: list[AtomFeedEntry] = []
        partial = False
        for page in entries_by_author:
            entries.extend(page.entries)
            partial = partial or page.partial
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
            partial=partial,
        )

    @_followed_profile_feed_cache
    async def _get_followed_profile_entries(
        self,
        user: SubstackFollowingUser,
        *,
        feed_type: Literal["mixed", "post", "note"],
        limit: int,
    ) -> AtomFeedEntriesPage:
        return await self._profile_feed.get_entries_for_profile_best_effort(
            user.id,
            fallback_author=AtomFeedAuthor(
                name=user.handle,
                handle=user.handle,
                avatar_url="",
            ),
            feed_type=feed_type,
            limit=limit,
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
