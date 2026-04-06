from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

import httpx
from typing_extensions import Self

from gateway_oss.client.exceptions import SubstackAPIError, SubstackAuthError
from gateway_oss.config import settings

_log = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(
    timeout=settings.substack_timeout_sec,
    connect=settings.substack_connect_timeout_sec,
)
_LIMITS = httpx.Limits(max_connections=20, max_keepalive_connections=5)
_RETRYABLE_STATUS_CODES = frozenset({408, 425, 429, 500, 502, 503, 504})


class _RequestRateLimiter:
    def __init__(self, rate_per_second: float) -> None:
        self.rate_per_second = rate_per_second
        self._interval = 1 / rate_per_second
        self._lock = asyncio.Lock()
        self._next_available_at = 0.0

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            delay = max(0.0, self._next_available_at - now)
            if delay > 0:
                await asyncio.sleep(delay)
                now = time.monotonic()
            self._next_available_at = max(self._next_available_at, now) + self._interval


_RATE_LIMITER = _RequestRateLimiter(settings.substack_requests_per_second)


def _get_rate_limiter() -> _RequestRateLimiter:
    global _RATE_LIMITER
    if _RATE_LIMITER.rate_per_second != settings.substack_requests_per_second:
        _RATE_LIMITER = _RequestRateLimiter(settings.substack_requests_per_second)
    return _RATE_LIMITER


def _retry_delay(attempt: int) -> float:
    return min(
        settings.substack_retry_max_wait_sec,
        settings.substack_retry_min_wait_sec * (2 ** (attempt - 1)),
    )


def _should_retry_status(status_code: int) -> bool:
    return status_code in _RETRYABLE_STATUS_CODES


class SubstackHTTPBase:
    """Raw HTTP layer shared by PublicationClient and SubstackClient."""

    _base: str  # set by each concrete subclass

    def __init__(
        self,
        substack_sid: str,
        connect_sid: str,
        request_id: str | None = None,
    ) -> None:
        self._cookies = {"substack.sid": substack_sid, "connect.sid": connect_sid}
        self._http: httpx.AsyncClient | None = None
        self._rid = f"[{request_id}] " if request_id else ""

    async def __aenter__(self) -> Self:
        self._http = httpx.AsyncClient(
            cookies=self._cookies, timeout=_TIMEOUT, limits=_LIMITS
        )
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None

    def _url(self, path: str) -> str:
        return f"{self._base}/{path.lstrip('/')}"

    async def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self._request("GET", self._url(path), **kwargs)

    async def post(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self._request("POST", self._url(path), **kwargs)

    async def put(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self._request("PUT", self._url(path), **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> httpx.Response:
        return await self._request("DELETE", self._url(path), **kwargs)

    async def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        if self._http is None:
            raise RuntimeError("Client must be used as an async context manager")
        max_attempts = settings.substack_retry_attempts

        for attempt in range(1, max_attempts + 1):
            await _get_rate_limiter().acquire()
            _log.debug(
                "%s→ %s %s (attempt %d/%d)",
                self._rid,
                method,
                url,
                attempt,
                max_attempts,
            )
            start = time.monotonic()
            try:
                r = await self._http.request(method, url, **kwargs)
            except httpx.TransportError as exc:
                elapsed = time.monotonic() - start
                if attempt < max_attempts:
                    delay = _retry_delay(attempt)
                    _log.warning(
                        "%sSubstack network error: %s %s — %s (%.3fs), retrying in %.3fs",
                        self._rid,
                        method,
                        url,
                        exc,
                        elapsed,
                        delay,
                    )
                    await asyncio.sleep(delay)
                    continue
                _log.warning(
                    "%sSubstack network error: %s %s — %s (%.3fs)",
                    self._rid,
                    method,
                    url,
                    exc,
                    elapsed,
                )
                raise SubstackAPIError(502, f"Network error: {exc}") from exc

            elapsed = time.monotonic() - start
            if r.status_code == 401:
                _log.warning(
                    "%s← %s %s → 401 Unauthorized (%.3fs)",
                    self._rid,
                    method,
                    url,
                    elapsed,
                )
                raise SubstackAuthError(
                    401, "Invalid or expired Substack session token"
                )
            if r.status_code == 403:
                _log.warning(
                    "%s← %s %s → 403 Forbidden (%.3fs)",
                    self._rid,
                    method,
                    url,
                    elapsed,
                )
                raise SubstackAuthError(
                    403, "Forbidden: insufficient permissions for this resource"
                )
            if _should_retry_status(r.status_code) and attempt < max_attempts:
                delay = _retry_delay(attempt)
                _log.warning(
                    "%s← %s %s → %d (%.3fs), retrying in %.3fs",
                    self._rid,
                    method,
                    url,
                    r.status_code,
                    elapsed,
                    delay,
                )
                await asyncio.sleep(delay)
                continue
            if not r.is_success:
                _log.warning(
                    "%s← %s %s → %d (%.3fs)",
                    self._rid,
                    method,
                    url,
                    r.status_code,
                    elapsed,
                )
                try:
                    body = r.json()
                    detail = (
                        body.get("error")
                        or body.get("message")
                        or f"HTTP {r.status_code}"
                    )
                except Exception:
                    detail = f"HTTP {r.status_code}"
                raise SubstackAPIError(
                    r.status_code, f"Substack returned {r.status_code}: {detail}"
                )
            _log.debug(
                "%s← %s %s → %d (%.3fs)",
                self._rid,
                method,
                url,
                r.status_code,
                elapsed,
            )
            return r

        raise RuntimeError("Request retry loop exited unexpectedly")
