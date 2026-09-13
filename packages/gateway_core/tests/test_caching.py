from __future__ import annotations

import pytest

from gateway_core.caching import (
    NullValueCache,
    get_value_cache,
    set_value_cache,
)


@pytest.fixture(autouse=True)
def _restore_registry():
    yield
    set_value_cache(None)


@pytest.mark.anyio
async def test_null_cache_calls_through_every_time() -> None:
    calls = []

    async def factory() -> str:
        calls.append(1)
        return "value"

    cache = NullValueCache()
    assert await cache.get_or_call("k", factory) == "value"
    assert await cache.get_or_call("k", factory) == "value"
    assert len(calls) == 2, "a null cache must never serve a stored answer"


def test_registry_defaults_to_the_null_cache() -> None:
    assert isinstance(get_value_cache(), NullValueCache)


def test_registry_returns_what_was_installed() -> None:
    class _Stub:
        async def get_or_call(self, key, factory):  # pragma: no cover - not called
            return None

    stub = _Stub()
    set_value_cache(stub)
    assert get_value_cache() is stub


def test_clearing_the_registry_restores_the_null_cache() -> None:
    class _Stub:
        async def get_or_call(self, key, factory):  # pragma: no cover - not called
            return None

    set_value_cache(_Stub())
    set_value_cache(None)
    assert isinstance(get_value_cache(), NullValueCache)
