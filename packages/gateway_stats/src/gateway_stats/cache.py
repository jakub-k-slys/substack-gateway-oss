from __future__ import annotations

from typing import Any

# A single timeseries row as returned by Substack: a positional list whose first
# element is the date bucket (e.g. ["2025/07/10", 1, 1, 0, 12]).
Row = list[Any]


class StatsCache:
    """Abstract cache for publication analytics.

    Two access shapes back the two kinds of stats data:

    * **timeseries** — append-only rows keyed by their date bucket. Historical
      rows never change, so subsequent calls only need to fetch the tail from
      Substack (delta fetch); the caller derives a watermark from
      :meth:`read_timeseries` and merges the new rows back via
      :meth:`write_timeseries` (an upsert, not a replace).
    * **snapshot** — an opaque JSON blob (summaries, aggregates).

    OSS ships no caching implementation — see :class:`NullStatsCache`, the
    default. An extension may install a real cache via :func:`set_stats_cache`;
    how long a cached value lives is that implementation's own policy.
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
        self, publication_url: str, key: str, value: dict[str, Any]
    ) -> None:
        """Store a snapshot under `key`."""
        raise NotImplementedError


class NullStatsCache(StatsCache):
    """The default: retains nothing, so every read is a miss.

    Every call therefore reaches Substack. That is the intended behaviour for a
    deployment with no cache installed, and it is the same path a cold cache
    takes on its first request.
    """

    async def read_timeseries(
        self, publication_url: str, series: str
    ) -> dict[str, Row]:
        return {}

    async def write_timeseries(
        self, publication_url: str, series: str, rows: dict[str, Row]
    ) -> None:
        return None

    async def get_snapshot(
        self, publication_url: str, key: str
    ) -> dict[str, Any] | None:
        return None

    async def set_snapshot(
        self, publication_url: str, key: str, value: dict[str, Any]
    ) -> None:
        return None


_stats_cache: StatsCache = NullStatsCache()


def set_stats_cache(cache: StatsCache | None) -> None:
    """Install the process-wide stats cache. ``None`` restores the null cache."""
    global _stats_cache
    _stats_cache = cache if cache is not None else NullStatsCache()


def get_stats_cache() -> StatsCache:
    """Return the installed stats cache. Never ``None`` — the null cache is the default."""
    return _stats_cache
