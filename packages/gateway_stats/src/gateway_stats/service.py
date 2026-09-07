from __future__ import annotations

import logging
from datetime import UTC, date, datetime, timedelta

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_core.config import settings
from gateway_stats.cache import Row, StatsCache

_log = logging.getLogger(__name__)

# Substack timeseries endpoints, keyed by the series name we cache under.
_TIMESERIES_ENDPOINTS: dict[str, str] = {
    "subscribers": "publication/stats/subscribers/timeseries",
}

_DEFAULT_LOOKBACK_DAYS = 365
_SNAPSHOT_30D_VIEWS = "traffic_30d_views"


def _default_from() -> str:
    return (datetime.now(UTC) - timedelta(days=_DEFAULT_LOOKBACK_DAYS)).strftime(
        "%Y-%m-%dT00:00:00Z"
    )


def _bucket_to_date(bucket: str) -> date:
    # Substack date buckets look like "2025/07/10".
    return datetime.strptime(bucket, "%Y/%m/%d").date()


def _iso_to_date(iso: str) -> date:
    # Accept "2025-07-10T10:52:11.615Z" or "2025-07-10"; only the day matters.
    return date.fromisoformat(iso[:10])


def _watermark_from(watermark: str, lag_days: int) -> str:
    """ISO ``from`` cursor: the watermark date minus a lag so maturing days are
    re-fetched and overwritten rather than frozen at stale values."""
    start = _bucket_to_date(watermark) - timedelta(days=lag_days)
    return start.strftime("%Y-%m-%dT00:00:00Z")


class StatsService:
    """Publication analytics, backed by a delta-aware cache.

    Timeseries are fetched incrementally: only rows newer than the cached
    watermark are pulled from Substack and merged. Snapshots are TTL-cached.
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

    async def subscriber_timeseries(self, from_: str | None = None) -> list[Row]:
        """Daily subscriber counts (paid / comps / free trials / total).

        Returns data rows (header stripped) sorted by date. Only the tail beyond
        the cached watermark is fetched from Substack on each call.
        """
        return await self._timeseries("subscribers", from_=from_)

    async def _timeseries(self, series: str, from_: str | None) -> list[Row]:
        path = _TIMESERIES_ENDPOINTS[series]
        cached = await self._cache.read_timeseries(self._pub_url, series)

        if cached:
            watermark = max(cached)  # "YYYY/MM/DD" strings sort chronologically
            fetch_from = _watermark_from(
                watermark, settings.stats_timeseries_watermark_lag_days
            )
        else:
            fetch_from = from_ or _default_from()

        _log.debug(
            "Fetching %s timeseries from=%s (cached_rows=%d)",
            series,
            fetch_from,
            len(cached),
        )
        r = await self._pub.get(path, params={"from": fetch_from})
        fresh = _rows_by_date(r.json())
        if fresh:
            await self._cache.write_timeseries(self._pub_url, series, fresh)

        merged = {**cached, **fresh}
        rows = [merged[bucket] for bucket in sorted(merged)]
        if from_:
            floor = _iso_to_date(from_)
            rows = [row for row in rows if _bucket_to_date(row[0]) >= floor]
        return rows

    async def thirty_day_views(self) -> dict[str, int]:
        """Trailing-30-day view count and its delta (snapshot, TTL-cached)."""
        cached = await self._cache.get_snapshot(self._pub_url, _SNAPSHOT_30D_VIEWS)
        if cached is not None:
            _log.debug("30d views served from snapshot cache")
            return cached

        r = await self._pub.get("publication/stats/publication_traffic/30d_views")
        data = r.json()
        await self._cache.set_snapshot(
            self._pub_url,
            _SNAPSHOT_30D_VIEWS,
            data,
            settings.stats_snapshot_cache_ttl_sec,
        )
        return data


def _rows_by_date(payload: object) -> dict[str, Row]:
    """Turn Substack's [header, *rows] timeseries payload into date→row.

    The first element is a header row of column labels; only rows whose first
    cell is a date bucket string are kept.
    """
    if not isinstance(payload, list) or len(payload) < 2:
        return {}
    result: dict[str, Row] = {}
    for row in payload[1:]:
        if isinstance(row, list) and row and isinstance(row[0], str):
            result[row[0]] = row
    return result
