from __future__ import annotations

from typing import Any, cast

import pytest
from _fakes import FakeStatsCache

from gateway_core.client.substack import SubstackClient
from gateway_stats.dashboard import DashboardService

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


def _service(pub: _FakePub, cache: FakeStatsCache | None = None) -> DashboardService:
    return DashboardService(
        cast(Any, pub),
        cast(SubstackClient, None),
        cache if cache is not None else FakeStatsCache(),
        PUB,
    )


@pytest.mark.anyio
async def test_summary_calls_upstream_and_caches():
    cache = FakeStatsCache()
    pub = _FakePub({"subscribers": 10})
    service = _service(pub, cache)

    data = await service.summary()

    assert data == {"subscribers": 10}
    assert pub.calls == [("publish-dashboard/summary", None)]
    assert cache.snapshots[(PUB, "dashboard_summary")] == {"subscribers": 10}

    await service.summary()
    assert len(pub.calls) == 1


@pytest.mark.anyio
async def test_period_passes_range_and_keys_by_it():
    cache = FakeStatsCache()
    pub = _FakePub({"views": 5})

    data = await _service(pub, cache).period(90)

    assert data == {"views": 5}
    assert pub.calls == [("publish-dashboard/summary-v2", {"range": 90})]
    assert (PUB, "dashboard_period:90") in cache.snapshots


@pytest.mark.anyio
async def test_post_counts_path_and_key():
    cache = FakeStatsCache()
    pub = _FakePub({"published": 3})

    data = await _service(pub, cache).post_counts()

    assert data == {"published": 3}
    assert pub.calls == [("post_management/counts", None)]
    assert (PUB, "post_counts") in cache.snapshots


_TARGET_PUB = {
    "id": 1001,
    "name": "Example Weekly",
    "subdomain": "exampleweekly",
    "custom_domain": None,
    "logo_url": "https://example.com/logo.png",
    "hero_text": "Long hero text",
    "theme": {"colors": ["#fff"]},
    "author_bio": "Bio",
}


@pytest.mark.anyio
async def test_recommendations_outgoing_slims_target_pub():
    cache = FakeStatsCache()
    pub = _FakePub(
        {
            "rows": [
                {
                    "publication_id": 1,
                    "target_publication_id": 1001,
                    "xp_signups": 7,
                    "is_mutual": True,
                    "irrelevant_blob": {"a": 1},
                    "target_pub": _TARGET_PUB,
                }
            ]
        }
    )

    data = await _service(pub, cache).recommendations("outgoing")

    row = data["rows"][0]
    assert row["pub"] == {
        "id": 1001,
        "name": "Example Weekly",
        "subdomain": "exampleweekly",
        "custom_domain": None,
        "logo_url": "https://example.com/logo.png",
    }
    assert "target_pub" not in row
    assert "irrelevant_blob" not in row
    assert row["xp_signups"] == 7
    assert "xp_paid_subs" not in row
    assert pub.calls == [("recommendations/stats/from", {"offset": 0, "limit": 20})]
    assert cache.snapshots[(PUB, "recommendations:outgoing:20:0")] == data


@pytest.mark.anyio
async def test_recommendations_incoming_uses_source_pub_and_to_path():
    pub = _FakePub({"rows": [{"publication_id": 2, "source_pub": _TARGET_PUB}]})

    data = await _service(pub).recommendations("incoming", offset=5, limit=10)

    assert data["rows"][0]["pub"]["id"] == 1001
    assert pub.calls == [("recommendations/stats/to", {"offset": 5, "limit": 10})]


@pytest.mark.anyio
async def test_recommendations_null_pub():
    pub = _FakePub({"rows": [{"xp_signups": 4, "target_pub": None}]})

    data = await _service(pub).recommendations("outgoing")

    assert data["rows"][0]["pub"] is None
    assert data["rows"][0]["xp_signups"] == 4


@pytest.mark.anyio
@pytest.mark.parametrize("payload", [{"rows": None}, {}])
async def test_recommendations_rows_null_or_missing(payload: dict[str, Any]):
    data = await _service(_FakePub(payload)).recommendations("outgoing")

    assert data == {"rows": []}


@pytest.mark.anyio
async def test_recommendations_rejects_unknown_direction():
    with pytest.raises(ValueError):
        await _service(_FakePub({})).recommendations("sideways")
