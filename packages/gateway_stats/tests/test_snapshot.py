from __future__ import annotations

from typing import Any

import pytest
from _fakes import FakeStatsCache

from gateway_stats.snapshot import cached_snapshot

PUB = "https://example.substack.com"


@pytest.mark.anyio
async def test_cached_snapshot_hit_skips_fetch() -> None:
    cache = FakeStatsCache()
    cache.snapshots[(PUB, "k")] = {"a": 1}

    async def fetch() -> dict[str, Any]:
        raise AssertionError("fetch must not run on a cache hit")

    assert await cached_snapshot(cache, PUB, "k", fetch) == {"a": 1}


@pytest.mark.anyio
async def test_cached_snapshot_miss_fetches_and_stores() -> None:
    cache = FakeStatsCache()
    calls = 0

    async def fetch() -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return {"b": 2}

    assert await cached_snapshot(cache, PUB, "k", fetch) == {"b": 2}
    assert calls == 1
    assert cache.snapshots[(PUB, "k")] == {"b": 2}
