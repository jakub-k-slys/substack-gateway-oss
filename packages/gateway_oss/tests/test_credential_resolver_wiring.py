from __future__ import annotations

from collections.abc import Sequence

import pytest

from gateway_core.auth import BearerCredentials
from gateway_core.credentials import get_credential_resolver, set_credential_resolver
from gateway_oss.extensions.base import GatewayExtensionContext, ModuleInfo
from substack_gateway import runtime
from substack_gateway.runtime import LifespanHook, _single_provider, get_runtime


class _Resolver:
    async def resolve(self, access_token: object) -> BearerCredentials | None:
        return None


class _ExtensionWithResolver:
    name = "with-resolver"

    def __init__(self, resolver: object) -> None:
        self._resolver = resolver

    def get_credential_resolver(self, context: GatewayExtensionContext) -> object:
        return self._resolver

    def get_lifespan_hooks(
        self, context: GatewayExtensionContext
    ) -> Sequence[LifespanHook]:
        return []

    def get_module_info(self, context: GatewayExtensionContext) -> ModuleInfo | None:
        return None


def test_single_provider_returns_the_only_resolver() -> None:
    resolver = _Resolver()
    assert _single_provider("credential resolver", [None, resolver]) is resolver


def test_single_provider_returns_none_when_no_extension_supplies_one() -> None:
    assert _single_provider("credential resolver", [None, None]) is None


def test_two_resolvers_is_a_startup_error() -> None:
    with pytest.raises(RuntimeError, match="credential resolver"):
        _single_provider("credential resolver", [_Resolver(), _Resolver()])


def test_protocol_default_returns_none() -> None:
    from gateway_oss.extensions.base import GatewayExtension

    class _Bare(GatewayExtension):
        name = "bare"

    context = GatewayExtensionContext(settings=None)  # ty: ignore[invalid-argument-type]
    assert _Bare().get_credential_resolver(context) is None


@pytest.fixture(autouse=True)
def _clear_resolver():
    set_credential_resolver(None)
    get_runtime.cache_clear()
    yield
    get_runtime.cache_clear()
    set_credential_resolver(None)


def test_extension_resolver_is_wired_into_gateway_core(monkeypatch) -> None:
    """The one link spanning the shell, gateway_oss, and gateway_core.

    An extension's `get_credential_resolver` result must end up installed as
    the process-wide resolver that `gateway_core.get_credential_resolver()`
    returns, not just be reachable in isolation via `_single_provider`.
    """
    resolver = _Resolver()
    extension = _ExtensionWithResolver(resolver)
    monkeypatch.setattr(runtime, "load_extensions", lambda: [extension])

    get_runtime.cache_clear()
    get_runtime()

    assert get_credential_resolver() is resolver
