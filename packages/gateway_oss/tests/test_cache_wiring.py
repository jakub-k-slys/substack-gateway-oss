from __future__ import annotations

from collections.abc import Sequence

import pytest

from gateway_core.caching import ValueCache, get_value_cache, set_value_cache
from gateway_oss.extensions.base import GatewayExtensionContext, ModuleInfo
from gateway_stats.cache import StatsCache, get_stats_cache, set_stats_cache
from substack_gateway import runtime
from substack_gateway.runtime import LifespanHook, _single_provider, get_runtime


def test_two_providers_is_a_startup_error() -> None:
    with pytest.raises(RuntimeError, match="Expected at most one value cache"):
        _single_provider("value cache", ["first", "second"])


def test_one_provider_is_selected() -> None:
    assert _single_provider("value cache", [None, "only"]) == "only"


def test_no_provider_selects_nothing() -> None:
    assert _single_provider("value cache", [None, None]) is None


def test_the_protocol_declares_both_hooks_with_none_defaults() -> None:
    from gateway_oss.extensions.base import GatewayExtension

    assert (
        GatewayExtension.get_value_cache(None, None)  # ty: ignore[invalid-argument-type]
        is None
    )
    assert (
        GatewayExtension.get_stats_cache(None, None)  # ty: ignore[invalid-argument-type]
        is None
    )


class _FakeValueCache:
    async def get_or_call(self, key, factory):  # type: ignore[no-untyped-def]
        return await factory()


class _FakeStatsCache(StatsCache):
    pass


class _ExtensionWithCaches:
    name = "with-caches"

    def __init__(self, value_cache: ValueCache, stats_cache: StatsCache) -> None:
        self._value_cache = value_cache
        self._stats_cache = stats_cache

    def get_value_cache(self, context: GatewayExtensionContext) -> ValueCache | None:
        return self._value_cache

    def get_stats_cache(self, context: GatewayExtensionContext) -> StatsCache | None:
        return self._stats_cache

    def get_lifespan_hooks(
        self, context: GatewayExtensionContext
    ) -> Sequence[LifespanHook]:
        return []

    def get_module_info(self, context: GatewayExtensionContext) -> ModuleInfo | None:
        return None


@pytest.fixture(autouse=True)
def _clear_caches():
    set_value_cache(None)
    set_stats_cache(None)
    get_runtime.cache_clear()
    yield
    get_runtime.cache_clear()
    set_value_cache(None)
    set_stats_cache(None)


def test_extension_caches_are_wired_into_gateway_core_and_gateway_stats(
    monkeypatch,
) -> None:
    """The one link spanning the shell, gateway_oss, gateway_core, and gateway_stats.

    An extension's `get_value_cache`/`get_stats_cache` results must end up
    installed as the process-wide caches that `gateway_core.get_value_cache()`
    and `gateway_stats.get_stats_cache()` return, not just be reachable in
    isolation via `_single_provider`.
    """
    value_cache = _FakeValueCache()
    stats_cache = _FakeStatsCache()
    extension = _ExtensionWithCaches(value_cache, stats_cache)
    monkeypatch.setattr(runtime, "load_extensions", lambda: [extension])

    get_runtime.cache_clear()
    get_runtime()

    assert get_value_cache() is value_cache
    assert get_stats_cache() is stats_cache
