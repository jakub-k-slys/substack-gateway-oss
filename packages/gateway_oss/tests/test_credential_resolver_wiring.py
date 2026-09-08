from __future__ import annotations

import pytest

from gateway_core.auth import BearerCredentials
from gateway_oss.extensions.base import GatewayExtensionContext
from substack_gateway.runtime import _single_provider


class _Resolver:
    async def resolve(self, access_token: object) -> BearerCredentials | None:
        return None


class _ExtensionWithResolver:
    name = "with-resolver"

    def __init__(self, resolver: object) -> None:
        self._resolver = resolver

    def get_credential_resolver(self, context: GatewayExtensionContext) -> object:
        return self._resolver


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
