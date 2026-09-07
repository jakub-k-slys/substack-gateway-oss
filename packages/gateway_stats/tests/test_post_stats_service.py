from __future__ import annotations

from typing import Any, cast

import pytest

from gateway_core.client.substack import SubstackClient
from gateway_stats.cache import InMemoryStatsCache
from gateway_stats.post_stats import PostStatsService

PUB = "https://example.substack.com"


class _FakeResponse:
    def __init__(self, payload: Any) -> None:
        self._payload = payload

    def json(self) -> Any:
        return self._payload


class _FakePub:
    def __init__(self, payload: Any) -> None:
        self._payload = payload
        self.calls: list[tuple[str, dict[str, Any] | None]] = []

    async def get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> _FakeResponse:
        self.calls.append((path, params))
        return _FakeResponse(self._payload)


def _service(pub: _FakePub) -> PostStatsService:
    return PostStatsService(
        cast(Any, pub), cast(SubstackClient, None), InMemoryStatsCache(), PUB
    )


@pytest.mark.anyio
async def test_engagement_hits_the_right_endpoint():
    pub = _FakePub({"likes": {"count": 3}})
    data = await _service(pub).engagement(42)

    assert data == {"likes": {"count": 3}}
    assert pub.calls[0][0] == "post_management/detail/42/engagement"


@pytest.mark.anyio
async def test_recipients_passes_pagination_params():
    pub = _FakePub({"rows": [], "total": 0})
    await _service(pub).recipients(42, limit=50, offset=10)

    assert pub.calls[0] == (
        "post_management/detail/42/recipients",
        {"limit": 50, "offset": 10},
    )


@pytest.mark.anyio
async def test_discussion_omits_cursor_when_absent_and_sends_when_present():
    pub1 = _FakePub({"items": []})
    await _service(pub1).discussion(42)
    assert pub1.calls[0][1] is None

    pub2 = _FakePub({"items": []})
    await _service(pub2).discussion(42, cursor="abc")
    assert pub2.calls[0][1] == {"cursor": "abc"}


@pytest.mark.anyio
async def test_snapshot_cache_avoids_second_upstream_call():
    cache = InMemoryStatsCache()
    pub = _FakePub({"referrers": [], "devices": [], "categories": []})
    service = PostStatsService(cast(Any, pub), cast(SubstackClient, None), cache, PUB)

    first = await service.traffic(7)
    second = await service.traffic(7)

    assert first == second
    assert len(pub.calls) == 1


@pytest.mark.anyio
async def test_recipients_pagination_is_cached_per_page():
    cache = InMemoryStatsCache()
    pub = _FakePub({"rows": [], "total": 0})
    service = PostStatsService(cast(Any, pub), cast(SubstackClient, None), cache, PUB)

    await service.recipients(7, limit=20, offset=0)
    await service.recipients(7, limit=20, offset=20)  # different page -> new fetch

    assert len(pub.calls) == 2
