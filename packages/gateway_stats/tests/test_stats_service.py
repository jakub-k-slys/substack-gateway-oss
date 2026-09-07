from __future__ import annotations

from typing import Any, cast

import pytest

from gateway_core.client.substack import SubstackClient
from gateway_core.config import settings
from gateway_stats.cache import InMemoryStatsCache
from gateway_stats.service import StatsService

PUB = "https://example.substack.com"

_HEADER = ["Date", "Paid", "Comps", "Free trials", "Total subscribers"]


class _FakeResponse:
    def __init__(self, payload: Any) -> None:
        self._payload = payload

    def json(self) -> Any:
        return self._payload


class _FakePub:
    """Records every GET and returns queued responses in order."""

    def __init__(self, responses: list[Any]) -> None:
        self._responses = list(responses)
        self.calls: list[tuple[str, dict[str, Any] | None]] = []

    async def get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> _FakeResponse:
        self.calls.append((path, params))
        return _FakeResponse(self._responses.pop(0))


def _make_service(pub: _FakePub, cache: InMemoryStatsCache) -> StatsService:
    return StatsService(cast(Any, pub), cast(SubstackClient, None), cache, PUB)


@pytest.mark.anyio
async def test_subscriber_timeseries_delta_fetches_only_the_tail(monkeypatch):
    monkeypatch.setattr(settings, "stats_timeseries_watermark_lag_days", 2)
    cache = InMemoryStatsCache()
    pub = _FakePub(
        [
            [_HEADER, ["2025/07/10", 1, 0, 0, 10], ["2025/07/11", 1, 0, 0, 11]],
            # second call: matured 07/11 (revised) + new 07/12
            [_HEADER, ["2025/07/11", 1, 0, 0, 12], ["2025/07/12", 2, 0, 0, 13]],
        ]
    )
    service = _make_service(pub, cache)

    first = await service.subscriber_timeseries(from_="2025-07-01T00:00:00Z")
    assert [r[0] for r in first] == ["2025/07/10", "2025/07/11"]
    assert pub.calls[0][1] == {"from": "2025-07-01T00:00:00Z"}

    second = await service.subscriber_timeseries()
    # watermark 2025/07/11 minus 2-day lag -> 2025-07-09
    assert pub.calls[1][1] == {"from": "2025-07-09T00:00:00Z"}
    # merged history: 07/10 kept, 07/11 overwritten with revised value, 07/12 new
    assert [r[0] for r in second] == ["2025/07/10", "2025/07/11", "2025/07/12"]
    assert second[1] == ["2025/07/11", 1, 0, 0, 12]


@pytest.mark.anyio
async def test_subscriber_timeseries_filters_by_from_bound():
    cache = InMemoryStatsCache()
    pub = _FakePub(
        [[_HEADER, ["2025/07/10", 1, 0, 0, 10], ["2025/07/11", 1, 0, 0, 11]]]
    )
    service = _make_service(pub, cache)

    rows = await service.subscriber_timeseries(from_="2025-07-11T00:00:00Z")

    assert [r[0] for r in rows] == ["2025/07/11"]


@pytest.mark.anyio
async def test_subscriber_timeseries_handles_empty_payload():
    cache = InMemoryStatsCache()
    pub = _FakePub([[_HEADER]])
    service = _make_service(pub, cache)

    rows = await service.subscriber_timeseries(from_="2025-07-01T00:00:00Z")

    assert rows == []


@pytest.mark.anyio
async def test_thirty_day_views_is_cached_after_first_fetch():
    cache = InMemoryStatsCache()
    pub = _FakePub([{"views30d": 100, "viewsDelta30d": 5}])
    service = _make_service(pub, cache)

    first = await service.thirty_day_views()
    second = await service.thirty_day_views()

    assert first == {"views30d": 100, "viewsDelta30d": 5}
    assert second == first
    # Only one upstream call — the second is served from the snapshot cache.
    assert len(pub.calls) == 1
