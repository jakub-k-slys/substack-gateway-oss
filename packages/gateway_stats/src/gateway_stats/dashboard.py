from __future__ import annotations

from enum import StrEnum
from typing import Any

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_stats.cache import StatsCache
from gateway_stats.snapshot import cached_snapshot

_SUMMARY = "publish-dashboard/summary"
_SUMMARY_V2 = "publish-dashboard/summary-v2"
_POST_COUNTS = "post_management/counts"

_ROW_KEYS = (
    "publication_id",
    "target_publication_id",
    "xp_signups",
    "xp_signups_last_30_days",
    "xp_paid_subs",
    "is_mutual",
    "is_active",
    "created_at",
    "first_activity_at",
    "data_updated_at",
)
_PUB_KEYS = ("id", "name", "subdomain", "custom_domain", "logo_url")


class RecommendationDirection(StrEnum):
    OUTGOING = "outgoing"
    INCOMING = "incoming"


_RECOMMENDATION_PATHS = {
    RecommendationDirection.OUTGOING: "recommendations/stats/from",
    RecommendationDirection.INCOMING: "recommendations/stats/to",
}


def _slim_pub(row: dict[str, Any], direction: str) -> dict[str, Any] | None:
    # The counterpart is the target publication for outgoing rows and the
    # source publication for incoming rows; the other key is this publication.
    if direction == RecommendationDirection.INCOMING:
        keys = ("source_pub", "target_pub")
    else:
        keys = ("target_pub", "source_pub")
    for key in keys:
        pub = row.get(key)
        if isinstance(pub, dict):
            return {k: pub[k] for k in _PUB_KEYS if k in pub}
    return None


def _slim_row(row: dict[str, Any], direction: str) -> dict[str, Any]:
    slim = {k: row[k] for k in _ROW_KEYS if k in row}
    slim["pub"] = _slim_pub(row, direction)
    return slim


class DashboardService:
    """Publication dashboard: summary, period summary, recommendations, post counts.

    Every call is an aggregate snapshot rather than an append-only series, so
    each is stored via :class:`StatsCache` snapshots keyed by endpoint (plus
    range/direction/pagination where relevant), through whatever cache is
    installed; with none installed, nothing is retained and every call
    reaches Substack. Recommendation rows are slimmed before caching. All
    calls hit the publication host.
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

    async def summary(self) -> dict[str, Any]:
        """Headline dashboard numbers for the publication."""

        async def fetch() -> dict[str, Any]:
            return (await self._pub.get(_SUMMARY)).json()

        return await cached_snapshot(
            self._cache, self._pub_url, "dashboard_summary", fetch
        )

    async def period(self, range_days: int = 365) -> dict[str, Any]:
        """Dashboard summary over the trailing ``range_days`` days."""

        async def fetch() -> dict[str, Any]:
            return (
                await self._pub.get(_SUMMARY_V2, params={"range": range_days})
            ).json()

        return await cached_snapshot(
            self._cache, self._pub_url, f"dashboard_period:{range_days}", fetch
        )

    async def recommendations(
        self,
        direction: RecommendationDirection | str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Recommendation stats, outgoing or incoming (paginated, slimmed rows)."""
        direction = RecommendationDirection(direction)

        async def fetch() -> dict[str, Any]:
            r = await self._pub.get(
                _RECOMMENDATION_PATHS[direction],
                params={"offset": offset, "limit": limit},
            )
            payload = r.json()
            rows = payload.get("rows") if isinstance(payload, dict) else None
            return {"rows": [_slim_row(row, direction) for row in rows or []]}

        return await cached_snapshot(
            self._cache,
            self._pub_url,
            f"recommendations:{direction}:{limit}:{offset}",
            fetch,
        )

    async def post_counts(self) -> dict[str, Any]:
        """Post counts by state (published, drafts, scheduled, ...)."""

        async def fetch() -> dict[str, Any]:
            return (await self._pub.get(_POST_COUNTS)).json()

        return await cached_snapshot(self._cache, self._pub_url, "post_counts", fetch)
