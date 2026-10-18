from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from gateway_stats.cache import StatsCache

_log = logging.getLogger(__name__)


async def cached_snapshot(
    cache: StatsCache,
    publication_url: str,
    key: str,
    fetch: Callable[[], Awaitable[dict[str, Any]]],
) -> dict[str, Any]:
    """Serve ``key`` from the snapshot cache, or fetch, store and return it."""
    cached = await cache.get_snapshot(publication_url, key)
    if cached is not None:
        _log.debug("%s served from snapshot cache", key)
        return cached
    data = await fetch()
    await cache.set_snapshot(publication_url, key, data)
    return data
