from __future__ import annotations

from typing import Any

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_stats.cache import StatsCache
from gateway_stats.snapshot import cached_snapshot

_DETAIL = "post_management/detail"


class PostStatsService:
    """Per-post analytics (the tabs of a published post's stats page).

    Every tab is an aggregate snapshot rather than an append-only series, so
    each is stored via :class:`StatsCache` snapshots keyed by post id (plus
    pagination/cursor where relevant), through whatever cache is installed;
    with none installed, nothing is retained and every call reaches
    Substack. All calls hit the publication host.
    """

    def __init__(
        self,
        pub: PublicationClient,
        sub: SubstackClient,
        cache: StatsCache,
        publication_url: str,
    ) -> None:
        self._pub = pub
        self._sub = sub
        self._cache = cache
        self._pub_url = publication_url

    async def _snapshot(
        self, key: str, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        async def fetch() -> dict[str, Any]:
            r = await self._pub.get(path, params=params)
            return r.json()

        return await cached_snapshot(self._cache, self._pub_url, key, fetch)

    async def engagement(self, post_id: int) -> dict[str, Any]:
        """Likes, comment summary, and commenters for a post."""
        return await self._snapshot(
            f"post:{post_id}:engagement", f"{_DETAIL}/{post_id}/engagement"
        )

    async def traffic(self, post_id: int) -> dict[str, Any]:
        """Referrers, devices, and category breakdown of a post's views."""
        return await self._snapshot(
            f"post:{post_id}:traffic", f"{_DETAIL}/{post_id}/traffic"
        )

    async def recipients(
        self, post_id: int, limit: int = 20, offset: int = 0
    ) -> dict[str, Any]:
        """Per-recipient email delivery / open / click rows (paginated)."""
        return await self._snapshot(
            f"post:{post_id}:recipients:{limit}:{offset}",
            f"{_DETAIL}/{post_id}/recipients",
            params={"limit": limit, "offset": offset},
        )

    async def growth(self, post_id: int) -> dict[str, Any]:
        """Subscriber growth attributed to a post."""
        return await self._snapshot(
            f"post:{post_id}:growth", f"{_DETAIL}/{post_id}/growth"
        )

    async def discussion(
        self, post_id: int, cursor: str | None = None
    ) -> dict[str, Any]:
        """Comment / discussion thread for a post (cursor-paginated)."""
        params = {"cursor": cursor} if cursor else None
        return await self._snapshot(
            f"post:{post_id}:discussion:{cursor or 'start'}",
            f"{_DETAIL}/{post_id}/discussion",
            params=params,
        )
