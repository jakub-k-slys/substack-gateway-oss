from __future__ import annotations

from collections.abc import Sequence

import httpx
import pytest

from gateway_core.client.transport import (
    default_transport_factory,
    get_transport_factory,
    set_transport_factory,
)
from gateway_oss.extensions.base import (
    GatewayExtension,
    GatewayExtensionContext,
    LifespanHook,
    ModuleInfo,
)
from substack_gateway import runtime
from substack_gateway.runtime import _single_provider, get_runtime


def _factory(limits: httpx.Limits) -> httpx.AsyncBaseTransport:
    return httpx.AsyncHTTPTransport(limits=limits)


def _other_factory(limits: httpx.Limits) -> httpx.AsyncBaseTransport:
    return httpx.AsyncHTTPTransport(limits=limits)


class _ExtensionWithFactory:
    def __init__(self, name: str, factory: object) -> None:
        self.name = name
        self._factory = factory

    def get_http_transport_factory(self, context: GatewayExtensionContext) -> object:
        return self._factory

    def get_lifespan_hooks(
        self, context: GatewayExtensionContext
    ) -> Sequence[LifespanHook]:
        return []

    def get_module_info(self, context: GatewayExtensionContext) -> ModuleInfo | None:
        return None


class _DuckTypedExtension:
    """Defines none of the optional hooks, as a non-subclassing extension may."""

    name = "duck"

    def get_lifespan_hooks(
        self, context: GatewayExtensionContext
    ) -> Sequence[LifespanHook]:
        return []

    def get_module_info(self, context: GatewayExtensionContext) -> ModuleInfo | None:
        return None


@pytest.fixture(autouse=True)
def _reset_transport_factory():
    set_transport_factory(None)
    get_runtime.cache_clear()
    yield
    get_runtime.cache_clear()
    set_transport_factory(None)


def test_protocol_default_returns_none() -> None:
    class _Bare(GatewayExtension):
        name = "bare"

    context = GatewayExtensionContext(settings=None)  # ty: ignore[invalid-argument-type]
    assert _Bare().get_http_transport_factory(context) is None


def test_extension_factory_is_installed(monkeypatch) -> None:
    extension = _ExtensionWithFactory("with-factory", _factory)
    monkeypatch.setattr(runtime, "load_extensions", lambda: [extension])

    result = get_runtime()

    assert get_transport_factory() is _factory
    assert result.transport_factory is _factory


def test_no_extension_keeps_default(monkeypatch) -> None:
    monkeypatch.setattr(runtime, "load_extensions", lambda: [])
    set_transport_factory(_other_factory)

    result = get_runtime()

    assert get_transport_factory() is default_transport_factory
    assert result.transport_factory is None


def test_two_factories_fail_startup(monkeypatch) -> None:
    extensions = [
        _ExtensionWithFactory("first", _factory),
        _ExtensionWithFactory("second", _other_factory),
    ]
    monkeypatch.setattr(runtime, "load_extensions", lambda: extensions)

    with pytest.raises(RuntimeError, match="HTTP transport factory"):
        get_runtime()


def test_duck_typed_extension_without_hook_is_tolerated(monkeypatch) -> None:
    monkeypatch.setattr(runtime, "load_extensions", lambda: [_DuckTypedExtension()])

    result = get_runtime()

    assert result.transport_factory is None
    assert get_transport_factory() is default_transport_factory


def test_single_provider_accepts_the_only_factory() -> None:
    assert _single_provider("HTTP transport factory", [None, _factory]) is _factory
