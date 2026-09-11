from __future__ import annotations

from typing import Any

from gateway_stats.cache import Row, StatsCache


class FakeStatsCache(StatsCache):
    """An in-memory StatsCache for tests. Not shipped — a double, not a cache."""

    def __init__(self) -> None:
        self.timeseries: dict[tuple[str, str], dict[str, Row]] = {}
        self.snapshots: dict[tuple[str, str], dict[str, Any]] = {}

    async def read_timeseries(
        self, publication_url: str, series: str
    ) -> dict[str, Row]:
        return dict(self.timeseries.get((publication_url, series), {}))

    async def write_timeseries(
        self, publication_url: str, series: str, rows: dict[str, Row]
    ) -> None:
        self.timeseries.setdefault((publication_url, series), {}).update(rows)

    async def get_snapshot(
        self, publication_url: str, key: str
    ) -> dict[str, Any] | None:
        return self.snapshots.get((publication_url, key))

    async def set_snapshot(
        self, publication_url: str, key: str, value: dict[str, Any]
    ) -> None:
        self.snapshots[(publication_url, key)] = value
