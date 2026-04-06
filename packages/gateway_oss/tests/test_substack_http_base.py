from __future__ import annotations

import time

import httpx
import pytest

from gateway_oss.client import base
from gateway_oss.client.base import SubstackHTTPBase
from gateway_oss.client.exceptions import SubstackAPIError, SubstackAuthError
from gateway_oss.config import settings


class _TestClient(SubstackHTTPBase):
    _base = "https://example.com/api/v1"


class _NoopRateLimiter:
    async def acquire(self) -> None:
        return None


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(autouse=True)
def _reset_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "substack_requests_per_second", 1000.0)
    monkeypatch.setattr(settings, "substack_retry_attempts", 3)
    monkeypatch.setattr(settings, "substack_retry_min_wait_sec", 1.0)
    monkeypatch.setattr(settings, "substack_retry_max_wait_sec", 60.0)
    monkeypatch.setattr(
        base,
        "_RATE_LIMITER",
        base._RequestRateLimiter(settings.substack_requests_per_second),
    )


@pytest.mark.anyio
async def test_request_retries_retryable_status_then_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    responses = [
        httpx.Response(503, json={"message": "busy"}),
        httpx.Response(200, json={"ok": True}),
    ]
    sleeps: list[float] = []

    async def fake_request(
        self: httpx.AsyncClient, method: str, url: str, **kwargs: object
    ) -> httpx.Response:
        return responses.pop(0)

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)
    monkeypatch.setattr(base.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(base, "_get_rate_limiter", lambda: _NoopRateLimiter())

    async with _TestClient("sid", "connect") as client:
        response = await client.get("posts")

    assert response.status_code == 200
    assert sleeps == [1.0]


@pytest.mark.anyio
async def test_request_retries_transport_error_then_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    attempts = 0
    sleeps: list[float] = []

    async def fake_request(
        self: httpx.AsyncClient, method: str, url: str, **kwargs: object
    ) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise httpx.ReadTimeout("timed out")
        return httpx.Response(200, json={"ok": True})

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)
    monkeypatch.setattr(base.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(base, "_get_rate_limiter", lambda: _NoopRateLimiter())

    async with _TestClient("sid", "connect") as client:
        response = await client.get("posts")

    assert response.status_code == 200
    assert attempts == 2
    assert sleeps == [1.0]


@pytest.mark.anyio
async def test_request_does_not_retry_auth_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    attempts = 0

    async def fake_request(
        self: httpx.AsyncClient, method: str, url: str, **kwargs: object
    ) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(401, json={"message": "unauthorized"})

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)
    monkeypatch.setattr(base, "_get_rate_limiter", lambda: _NoopRateLimiter())

    async with _TestClient("sid", "connect") as client:
        with pytest.raises(SubstackAuthError, match="Invalid or expired"):
            await client.get("posts")

    assert attempts == 1


@pytest.mark.anyio
async def test_request_raises_after_retry_budget_exhausted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def fake_request(
        self: httpx.AsyncClient, method: str, url: str, **kwargs: object
    ) -> httpx.Response:
        return httpx.Response(503, json={"message": "still busy"})

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)
    monkeypatch.setattr(base.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(base, "_get_rate_limiter", lambda: _NoopRateLimiter())

    async with _TestClient("sid", "connect") as client:
        with pytest.raises(SubstackAPIError, match="Substack returned 503: still busy"):
            await client.get("posts")

    assert sleeps == [1.0, 2.0]


@pytest.mark.anyio
async def test_rate_limiter_delays_subsequent_calls() -> None:
    limiter = base._RequestRateLimiter(100.0)

    start = time.monotonic()
    await limiter.acquire()
    await limiter.acquire()
    elapsed = time.monotonic() - start

    assert elapsed >= 0.009
