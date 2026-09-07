from __future__ import annotations

import pytest

import gateway_stats.cache as stats_cache_mod
from gateway_core.config import settings
from gateway_stats.cache import (
    InMemoryStatsCache,
    RedisStatsCache,
    create_stats_cache,
)

PUB = "https://example.substack.com"


@pytest.fixture(autouse=True)
def reset_factory_singleton(monkeypatch):
    monkeypatch.setattr(stats_cache_mod, "_default_cache", None)
    yield


def test_factory_returns_in_memory_when_redis_url_is_unset(monkeypatch):
    monkeypatch.setattr(settings, "redis_url", None)

    cache = create_stats_cache()

    assert isinstance(cache, InMemoryStatsCache)


def test_factory_returns_redis_when_redis_url_is_set(monkeypatch):
    monkeypatch.setattr(settings, "redis_url", "redis://localhost:6379/0")

    cache = create_stats_cache()

    assert isinstance(cache, RedisStatsCache)


def test_factory_is_singleton(monkeypatch):
    monkeypatch.setattr(settings, "redis_url", None)

    first = create_stats_cache()
    second = create_stats_cache()

    assert first is second


@pytest.mark.anyio
async def test_timeseries_write_merges_and_read_returns_copy():
    cache = InMemoryStatsCache()

    await cache.write_timeseries(PUB, "subscribers", {"2025/07/10": ["2025/07/10", 1]})
    await cache.write_timeseries(PUB, "subscribers", {"2025/07/11": ["2025/07/11", 2]})

    rows = await cache.read_timeseries(PUB, "subscribers")
    assert sorted(rows) == ["2025/07/10", "2025/07/11"]

    # Mutating the returned dict must not corrupt cached state.
    rows["2025/07/12"] = ["x"]
    again = await cache.read_timeseries(PUB, "subscribers")
    assert "2025/07/12" not in again


@pytest.mark.anyio
async def test_timeseries_write_overwrites_maturing_day():
    cache = InMemoryStatsCache()

    await cache.write_timeseries(PUB, "subscribers", {"2025/07/10": ["2025/07/10", 1]})
    await cache.write_timeseries(PUB, "subscribers", {"2025/07/10": ["2025/07/10", 5]})

    rows = await cache.read_timeseries(PUB, "subscribers")
    assert rows["2025/07/10"] == ["2025/07/10", 5]


@pytest.mark.anyio
async def test_timeseries_is_scoped_per_publication():
    cache = InMemoryStatsCache()

    await cache.write_timeseries(PUB, "subscribers", {"2025/07/10": ["2025/07/10", 1]})

    other = await cache.read_timeseries("https://other.substack.com", "subscribers")
    assert other == {}


@pytest.mark.anyio
async def test_snapshot_roundtrip_and_expiry():
    clock = {"now": 1000.0}
    cache = InMemoryStatsCache(time_fn=lambda: clock["now"])

    await cache.set_snapshot(PUB, "views", {"views30d": 42}, ttl_sec=60)
    assert await cache.get_snapshot(PUB, "views") == {"views30d": 42}

    clock["now"] = 1000.0 + 61  # advance past TTL
    assert await cache.get_snapshot(PUB, "views") is None
