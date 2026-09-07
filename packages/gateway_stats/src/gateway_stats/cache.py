from __future__ import annotations

import asyncio
import json
import logging
import time
from collections.abc import Callable
from typing import Any

from gateway_core.config import settings

_log = logging.getLogger(__name__)

# A single timeseries row as returned by Substack: a positional list whose first
# element is the date bucket (e.g. ["2025/07/10", 1, 1, 0, 12]).
Row = list[Any]

_NAMESPACE = "sgw:stats"


def _ts_key(publication_url: str, series: str) -> str:
    return f"{_NAMESPACE}:ts:{publication_url}:{series}"


def _snap_key(publication_url: str, key: str) -> str:
    return f"{_NAMESPACE}:snap:{publication_url}:{key}"


class StatsCache:
    """Abstract cache for publication analytics.

    Two access shapes back the two kinds of stats data:

    * **timeseries** — append-only rows keyed by their date bucket. Historical
      rows never change, so subsequent calls only need to fetch the tail from
      Substack (delta fetch); the caller derives a watermark from
      :meth:`read_timeseries` and merges the new rows back via
      :meth:`write_timeseries` (an upsert, not a replace).
    * **snapshot** — an opaque JSON blob (summaries, aggregates) with a TTL.

    Two implementations ship: :class:`RedisStatsCache` (Redis / Dragonfly) and
    :class:`InMemoryStatsCache` (process-local fallback for dev/tests). The
    factory :func:`create_stats_cache` picks one based on
    ``SUBSTACK_GATEWAY_REDIS_URL``.
    """

    async def read_timeseries(
        self, publication_url: str, series: str
    ) -> dict[str, Row]:
        """Return cached rows keyed by date bucket ({} when nothing cached)."""
        raise NotImplementedError

    async def write_timeseries(
        self, publication_url: str, series: str, rows: dict[str, Row]
    ) -> None:
        """Upsert (merge) the given date→row mapping into the cached series."""
        raise NotImplementedError

    async def get_snapshot(
        self, publication_url: str, key: str
    ) -> dict[str, Any] | None:
        """Return a cached snapshot, or None when absent/expired."""
        raise NotImplementedError

    async def set_snapshot(
        self, publication_url: str, key: str, value: dict[str, Any], ttl_sec: int
    ) -> None:
        """Store a snapshot under `key` with a TTL."""
        raise NotImplementedError


class RedisStatsCache(StatsCache):
    """Redis / Dragonfly-backed cache.

    Timeseries live in a Hash (field = date bucket, value = JSON row) so a
    single ``HSET`` upserts the tail and overwrites maturing days idempotently.
    Snapshots are plain strings with an ``EX`` TTL.
    """

    def __init__(self, redis_url: str) -> None:
        # Imported lazily so the module stays importable without a live server.
        import redis.asyncio as redis

        self._redis = redis.from_url(redis_url, decode_responses=True)

    async def read_timeseries(
        self, publication_url: str, series: str
    ) -> dict[str, Row]:
        raw = await self._redis.hgetall(_ts_key(publication_url, series))
        return {str(date): json.loads(row) for date, row in raw.items()}

    async def write_timeseries(
        self, publication_url: str, series: str, rows: dict[str, Row]
    ) -> None:
        if not rows:
            return
        key = _ts_key(publication_url, series)
        await self._redis.hset(
            key, mapping={date: json.dumps(row) for date, row in rows.items()}
        )
        await self._redis.expire(key, settings.stats_timeseries_ttl_sec)

    async def get_snapshot(
        self, publication_url: str, key: str
    ) -> dict[str, Any] | None:
        raw = await self._redis.get(_snap_key(publication_url, key))
        return json.loads(raw) if raw is not None else None

    async def set_snapshot(
        self, publication_url: str, key: str, value: dict[str, Any], ttl_sec: int
    ) -> None:
        await self._redis.set(
            _snap_key(publication_url, key), json.dumps(value), ex=ttl_sec
        )


class InMemoryStatsCache(StatsCache):
    """Process-local fallback used when no REDIS_URL is configured.

    State is per-process and lost on restart — matches how the OSS gateway
    treats other non-Substack state today. `time_fn` is injectable so tests can
    exercise snapshot expiry deterministically.
    """

    def __init__(self, time_fn: Callable[[], float] = time.monotonic) -> None:
        self._timeseries: dict[str, dict[str, Row]] = {}
        self._snapshots: dict[str, tuple[dict[str, Any], float]] = {}
        self._time = time_fn
        self._lock = asyncio.Lock()

    async def read_timeseries(
        self, publication_url: str, series: str
    ) -> dict[str, Row]:
        async with self._lock:
            return dict(self._timeseries.get(_ts_key(publication_url, series), {}))

    async def write_timeseries(
        self, publication_url: str, series: str, rows: dict[str, Row]
    ) -> None:
        if not rows:
            return
        async with self._lock:
            self._timeseries.setdefault(_ts_key(publication_url, series), {}).update(
                rows
            )

    async def get_snapshot(
        self, publication_url: str, key: str
    ) -> dict[str, Any] | None:
        async with self._lock:
            entry = self._snapshots.get(_snap_key(publication_url, key))
            if entry is None:
                return None
            value, expires_at = entry
            if self._time() >= expires_at:
                self._snapshots.pop(_snap_key(publication_url, key), None)
                return None
            return dict(value)

    async def set_snapshot(
        self, publication_url: str, key: str, value: dict[str, Any], ttl_sec: int
    ) -> None:
        async with self._lock:
            self._snapshots[_snap_key(publication_url, key)] = (
                dict(value),
                self._time() + ttl_sec,
            )


_default_cache: StatsCache | None = None


def create_stats_cache() -> StatsCache:
    """Return the process-wide stats cache instance.

    Uses :class:`RedisStatsCache` when ``SUBSTACK_GATEWAY_REDIS_URL`` is
    configured, otherwise an in-memory fallback shared across requests.
    """
    global _default_cache
    if _default_cache is None:
        if settings.redis_url:
            _default_cache = RedisStatsCache(settings.redis_url)
        else:
            _log.warning(
                "REDIS_URL not configured; using in-memory stats cache "
                "(state is not shared across processes and is lost on restart)."
            )
            _default_cache = InMemoryStatsCache()
    return _default_cache
