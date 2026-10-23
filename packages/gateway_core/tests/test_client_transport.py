from __future__ import annotations

from collections.abc import Iterator

import httpx
import pytest

from gateway_core.client.base import _get_limits
from gateway_core.client.substack import SubstackClient
from gateway_core.client.transport import (
    default_transport_factory,
    get_transport_factory,
    set_transport_factory,
)


@pytest.fixture(autouse=True)
def _reset_transport_factory() -> Iterator[None]:
    yield
    set_transport_factory(None)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def test_default_factory_is_http_transport_with_limits() -> None:
    limits = httpx.Limits(max_connections=3, max_keepalive_connections=1)

    transport = get_transport_factory()(limits)

    assert isinstance(transport, httpx.AsyncHTTPTransport)


@pytest.mark.anyio
async def test_installed_factory_receives_limits_and_serves_requests() -> None:
    received: list[httpx.Limits] = []

    def factory(limits: httpx.Limits) -> httpx.AsyncBaseTransport:
        received.append(limits)
        return httpx.MockTransport(
            lambda request: httpx.Response(200, json={"ok": True})
        )

    set_transport_factory(factory)

    async with SubstackClient("a", "b") as client:
        response = await client.get("x")

    assert response.json() == {"ok": True}
    assert received == [_get_limits()]


def test_reset_restores_default() -> None:
    set_transport_factory(
        lambda limits: httpx.MockTransport(lambda request: httpx.Response(200))
    )
    assert get_transport_factory() is not default_transport_factory

    set_transport_factory(None)

    assert get_transport_factory() is default_transport_factory


@pytest.mark.anyio
async def test_default_path_honours_env_proxies(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in ("ALL_PROXY", "HTTP_PROXY", "NO_PROXY", "all_proxy", "http_proxy"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.invalid:3128")

    async with SubstackClient("a", "b") as client:
        assert client._http is not None
        # httpx mounts one transport per proxied URL pattern when it reads the
        # environment; with an explicit transport it mounts none.
        patterns = [pattern.pattern for pattern in client._http._mounts]

    assert any(pattern.startswith("https") for pattern in patterns)
