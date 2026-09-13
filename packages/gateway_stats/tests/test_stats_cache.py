from __future__ import annotations

import pytest

from gateway_stats.cache import NullStatsCache, get_stats_cache, set_stats_cache

PUB = "https://example.substack.com"


@pytest.fixture(autouse=True)
def _restore_registry():
    yield
    set_stats_cache(None)


@pytest.mark.anyio
async def test_null_cache_never_retains_timeseries() -> None:
    cache = NullStatsCache()
    await cache.write_timeseries(PUB, "subscribers", {"2025/07/10": ["2025/07/10", 1]})
    assert await cache.read_timeseries(PUB, "subscribers") == {}


@pytest.mark.anyio
async def test_null_cache_never_retains_snapshots() -> None:
    cache = NullStatsCache()
    await cache.set_snapshot(PUB, "views", {"total": 1})
    assert await cache.get_snapshot(PUB, "views") is None


def test_registry_defaults_to_the_null_cache() -> None:
    assert isinstance(get_stats_cache(), NullStatsCache)


def test_registry_returns_what_was_installed() -> None:
    stub = NullStatsCache()
    set_stats_cache(stub)
    assert get_stats_cache() is stub


def test_clearing_the_registry_restores_the_null_cache() -> None:
    set_stats_cache(NullStatsCache())
    set_stats_cache(None)
    assert isinstance(get_stats_cache(), NullStatsCache)
