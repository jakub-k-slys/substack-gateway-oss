from __future__ import annotations

from typing import Any, cast

import pytest

from gateway_core.caching import set_value_cache
from gateway_core.client.substack import SubstackClient
from gateway_profiles.service import ProfilesService

_PAYLOAD = {"id": 7, "name": "Example", "handle": "example"}


class _FakeResponse:
    def json(self) -> Any:
        return _PAYLOAD


class _FakeSub:
    def __init__(self) -> None:
        self.calls: list[str] = []

    async def get(self, path: str) -> _FakeResponse:
        self.calls.append(path)
        return _FakeResponse()


class _RecordingCache:
    """A cache that stores forever and records the keys it was asked for."""

    def __init__(self) -> None:
        self.keys: list[str] = []
        self._values: dict[str, Any] = {}

    async def get_or_call(self, key, factory):
        self.keys.append(key)
        if key not in self._values:
            self._values[key] = await factory()
        return self._values[key]


@pytest.fixture(autouse=True)
def _restore_registry():
    yield
    set_value_cache(None)


@pytest.mark.anyio
async def test_without_a_cache_every_lookup_reaches_substack() -> None:
    sub = _FakeSub()
    service = ProfilesService(cast(SubstackClient, sub))
    await service.get_profile_by_slug("example")
    await service.get_profile_by_slug("example")
    assert len(sub.calls) == 2


@pytest.mark.anyio
async def test_an_installed_cache_is_used() -> None:
    cache = _RecordingCache()
    set_value_cache(cache)
    sub = _FakeSub()
    service = ProfilesService(cast(SubstackClient, sub))
    await service.get_profile_by_slug("example")
    await service.get_profile_by_slug("example")
    assert len(sub.calls) == 1


@pytest.mark.anyio
async def test_the_key_is_the_slug_not_the_service_instance() -> None:
    cache = _RecordingCache()
    set_value_cache(cache)
    await ProfilesService(cast(SubstackClient, _FakeSub())).get_profile_by_slug("a")
    await ProfilesService(cast(SubstackClient, _FakeSub())).get_profile_by_slug("a")
    assert cache.keys[0] == cache.keys[1], (
        "two service instances must share one cache key, or the cache is useless"
    )
    assert "a" in cache.keys[0]
