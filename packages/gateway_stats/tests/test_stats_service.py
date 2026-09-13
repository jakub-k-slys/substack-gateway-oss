from __future__ import annotations

from typing import Any, cast

import pytest
from _fakes import FakeStatsCache

from gateway_core.client.substack import SubstackClient
from gateway_core.config import settings
from gateway_stats.cache import StatsCache
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


def _make_service(pub: _FakePub, cache: StatsCache) -> StatsService:
    return StatsService(cast(Any, pub), cast(SubstackClient, None), cache, PUB)


@pytest.mark.anyio
async def test_subscriber_timeseries_delta_fetches_only_the_tail(monkeypatch):
    monkeypatch.setattr(settings, "stats_timeseries_watermark_lag_days", 2)
    cache = FakeStatsCache()
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
    cache = FakeStatsCache()
    pub = _FakePub(
        [[_HEADER, ["2025/07/10", 1, 0, 0, 10], ["2025/07/11", 1, 0, 0, 11]]]
    )
    service = _make_service(pub, cache)

    rows = await service.subscriber_timeseries(from_="2025-07-11T00:00:00Z")

    assert [r[0] for r in rows] == ["2025/07/11"]


@pytest.mark.anyio
async def test_subscriber_timeseries_handles_empty_payload():
    cache = FakeStatsCache()
    pub = _FakePub([[_HEADER]])
    service = _make_service(pub, cache)

    rows = await service.subscriber_timeseries(from_="2025-07-01T00:00:00Z")

    assert rows == []


@pytest.mark.anyio
async def test_thirty_day_views_is_cached_after_first_fetch():
    cache = FakeStatsCache()
    pub = _FakePub([{"views30d": 100, "viewsDelta30d": 5}])
    service = _make_service(pub, cache)

    first = await service.thirty_day_views()
    second = await service.thirty_day_views()

    assert first == {"views30d": 100, "viewsDelta30d": 5}
    assert second == first
    # Only one upstream call — the second is served from the snapshot cache.
    assert len(pub.calls) == 1


@pytest.mark.anyio
async def test_default_window_is_seven_days(monkeypatch) -> None:
    from gateway_stats import service as service_mod

    assert service_mod._DEFAULT_LOOKBACK_DAYS == 7


@pytest.mark.anyio
async def test_a_warm_cache_widens_when_asked_for_older_data(monkeypatch) -> None:
    monkeypatch.setattr(settings, "stats_timeseries_watermark_lag_days", 2)
    cache = FakeStatsCache()
    await cache.write_timeseries(
        PUB, "subscribers", {"2025/07/10": ["2025/07/10", 1, 0, 0, 10]}
    )
    pub = _FakePub([[_HEADER, ["2025/01/01", 1, 0, 0, 5]]])
    service = _make_service(pub, cache)

    await service.subscriber_timeseries(from_="2025-01-01T00:00:00Z")

    _path, params = pub.calls[0]
    assert params == {"from": "2025-01-01T00:00:00Z"}, (
        "a from_ older than the oldest cached row must widen the fetch, "
        "not be reduced to a filter over rows already held"
    )


@pytest.mark.anyio
async def test_without_a_cache_from_is_honoured_every_call() -> None:
    from gateway_stats.cache import NullStatsCache

    pub = _FakePub(
        [
            [_HEADER, ["2025/01/01", 1, 0, 0, 5]],
            [_HEADER, ["2025/01/01", 1, 0, 0, 5]],
        ]
    )
    service = _make_service(pub, NullStatsCache())

    first = await service.subscriber_timeseries(from_="2025-01-01T00:00:00Z")
    await service.subscriber_timeseries(from_="2025-01-01T00:00:00Z")

    assert first == [["2025/01/01", 1, 0, 0, 5]], (
        "an uncached deployment must still return the rows it fetched"
    )
    assert [params for _path, params in pub.calls] == [
        {"from": "2025-01-01T00:00:00Z"},
        {"from": "2025-01-01T00:00:00Z"},
    ], "with nothing retained, every call fetches the window the caller asked for"


@pytest.mark.anyio
async def test_a_warm_cache_still_delta_fetches_when_from_is_inside_it(
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, "stats_timeseries_watermark_lag_days", 2)
    cache = FakeStatsCache()
    await cache.write_timeseries(
        PUB,
        "subscribers",
        {
            "2025/07/10": ["2025/07/10", 1, 0, 0, 10],
            "2025/07/11": ["2025/07/11", 1, 0, 0, 11],
        },
    )
    pub = _FakePub([[_HEADER, ["2025/07/12", 1, 0, 0, 12]]])
    service = _make_service(pub, cache)

    await service.subscriber_timeseries(from_="2025-07-11T00:00:00Z")

    _path, params = pub.calls[0]
    assert params == {"from": "2025-07-09T00:00:00Z"}, (
        "a from_ inside the cached range must leave the watermark path alone"
    )


@pytest.mark.anyio
async def test_widening_never_fetches_less_than_the_watermark_path_would(
    monkeypatch,
) -> None:
    # Cache span is short (2025/07/01 - 2025/07/20) relative to a large
    # watermark_lag_days (30), so the watermark-derived date (2025-06-20) is
    # already earlier than `from_` (2025-06-25), which is itself older than
    # the oldest cached row (2025/07/01). Widening must still fire, but it
    # must land on the EARLIER of the two dates -- the watermark date -- not
    # overwrite it with the later `from_` and silently shrink the maturing
    # re-fetch window.
    monkeypatch.setattr(settings, "stats_timeseries_watermark_lag_days", 30)
    cache = FakeStatsCache()
    await cache.write_timeseries(
        PUB,
        "subscribers",
        {
            "2025/07/01": ["2025/07/01", 1, 0, 0, 1],
            "2025/07/20": ["2025/07/20", 1, 0, 0, 20],
        },
    )
    pub = _FakePub([[_HEADER, ["2025/06/20", 1, 0, 0, 0]]])
    service = _make_service(pub, cache)

    await service.subscriber_timeseries(from_="2025-06-25T00:00:00Z")

    _path, params = pub.calls[0]
    assert params == {"from": "2025-06-20T00:00:00Z"}, (
        "the fetch must start at the watermark date (the earlier of the two), "
        "not at from_, or part of the maturing re-fetch window is silently lost"
    )
