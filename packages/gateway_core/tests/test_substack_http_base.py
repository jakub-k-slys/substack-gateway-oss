from __future__ import annotations

import time

import httpx
import pytest

from gateway_core.client import base
from gateway_core.client.base import SubstackHTTPBase
from gateway_core.client.exceptions import SubstackAPIError, SubstackAuthError
from gateway_core.config import settings


class _TestClient(SubstackHTTPBase):
    _base = "https://example.com/api/v1"


class _NoopRateLimiter:
    def try_acquire(
        self, name: str = "substack_api", weight: int = 1, blocking: bool = True
    ) -> bool:
        return True

    def as_decorator(self, *, name: str = "substack_api", weight: int = 1):
        def _decorate(func):
            async def _wrapped(*args, **kwargs):
                acquired = self.try_acquire(name=name, weight=weight, blocking=True)
                if hasattr(acquired, "__await__"):
                    await acquired
                return await func(*args, **kwargs)

            return _wrapped

        return _decorate


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
        base._build_rate_limiter(),
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
    monkeypatch.setattr(base, "_sleep", fake_sleep)
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
    monkeypatch.setattr(base, "_sleep", fake_sleep)
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
    monkeypatch.setattr(base, "_sleep", fake_sleep)
    monkeypatch.setattr(base, "_get_rate_limiter", lambda: _NoopRateLimiter())

    async with _TestClient("sid", "connect") as client:
        with pytest.raises(SubstackAPIError, match="Substack returned 503: still busy"):
            await client.get("posts")

    assert sleeps == [1.0, 2.0]


@pytest.mark.anyio
async def test_rate_limiter_delays_subsequent_calls() -> None:
    limiter = base.Limiter(base.Rate(1, base.Duration.SECOND))

    start = time.monotonic()
    acquired = limiter.try_acquire("substack_api", blocking=True)
    if hasattr(acquired, "__await__"):
        await acquired
    acquired = limiter.try_acquire("substack_api", blocking=True)
    if hasattr(acquired, "__await__"):
        await acquired
    elapsed = time.monotonic() - start

    assert elapsed >= 0.9


# --- Write requests: retry only when Substack cannot have processed them ----


def _install_fake(
    monkeypatch: pytest.MonkeyPatch, outcomes: list[httpx.Response | Exception]
) -> list[str]:
    """Replay `outcomes` (a response, or an exception to raise) and record methods."""
    calls: list[str] = []

    async def fake_request(
        self: httpx.AsyncClient, method: str, url: str, **kwargs: object
    ) -> httpx.Response:
        calls.append(method)
        outcome = outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    async def fake_sleep(delay: float) -> None:
        return None

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)
    monkeypatch.setattr(base, "_sleep", fake_sleep)
    monkeypatch.setattr(base, "_get_rate_limiter", lambda: _NoopRateLimiter())
    return calls


@pytest.mark.anyio
@pytest.mark.parametrize("method", ["post", "put", "delete"])
@pytest.mark.parametrize("status", [408, 500, 502, 503, 504])
async def test_write_is_not_retried_on_ambiguous_status(
    monkeypatch: pytest.MonkeyPatch, method: str, status: int
) -> None:
    calls = _install_fake(monkeypatch, [httpx.Response(status, json={})])

    async with _TestClient("sid", "connect") as client:
        with pytest.raises(SubstackAPIError):
            await getattr(client, method)("messages/dm/x")

    assert calls == [method.upper()]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "error",
    [httpx.ReadTimeout("timed out"), httpx.ReadError("reset"), httpx.WriteTimeout("t")],
)
async def test_write_is_not_retried_after_the_request_may_have_been_sent(
    monkeypatch: pytest.MonkeyPatch, error: Exception
) -> None:
    calls = _install_fake(monkeypatch, [error])

    async with _TestClient("sid", "connect") as client:
        with pytest.raises(SubstackAPIError, match="Network error"):
            await client.post("messages/dm/x", json={"body": "hi"})

    assert calls == ["POST"]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "first",
    [
        httpx.ConnectError("refused"),
        httpx.ConnectTimeout("connect timed out"),
        httpx.PoolTimeout("pool exhausted"),
        httpx.Response(429, json={}),
        httpx.Response(425, json={}),
    ],
)
async def test_write_is_retried_when_substack_cannot_have_processed_it(
    monkeypatch: pytest.MonkeyPatch, first: httpx.Response | Exception
) -> None:
    calls = _install_fake(monkeypatch, [first, httpx.Response(200, json={"ok": True})])

    async with _TestClient("sid", "connect") as client:
        response = await client.post("messages/dm/x", json={"body": "hi"})

    assert response.status_code == 200
    assert calls == ["POST", "POST"]


@pytest.mark.anyio
async def test_read_is_still_retried_on_ambiguous_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _install_fake(
        monkeypatch,
        [
            httpx.Response(504, json={}),
            httpx.ReadTimeout("timed out"),
            httpx.Response(200, json={"ok": True}),
        ],
    )

    async with _TestClient("sid", "connect") as client:
        response = await client.get("posts")

    assert response.status_code == 200
    assert calls == ["GET", "GET", "GET"]
