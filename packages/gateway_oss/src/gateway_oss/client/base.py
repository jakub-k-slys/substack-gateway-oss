from __future__ import annotations

import asyncio
import inspect
import logging
import math
import time
from collections.abc import Callable
from typing import Any

import httpx
from pyrate_limiter import Duration, Limiter, Rate
from tenacity import (
    AsyncRetrying,
    RetryCallState,
    retry_if_exception,
    stop_after_attempt,
)
from tenacity.wait import wait_exponential
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


class RetryableSubstackError(Exception):
    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        super().__init__(f"Retryable HTTP status {response.status_code}")


async def _sleep(seconds: float) -> None:
    await asyncio.sleep(seconds)


def _build_rate_limiter() -> Limiter:
    per_second = max(1, math.ceil(settings.substack_requests_per_second))
    return Limiter(Rate(per_second, Duration.SECOND))


_RATE_LIMITER = _build_rate_limiter()


def _get_rate_limiter() -> Limiter:
    global _RATE_LIMITER
    expected_rate = max(1, math.ceil(settings.substack_requests_per_second))
    bucket = getattr(getattr(_RATE_LIMITER, "bucket_factory", None), "bucket", None)
    rates = getattr(bucket, "rates", None)
    current_rate = rates[0].limit if rates else None
    if current_rate != expected_rate:
        _RATE_LIMITER = _build_rate_limiter()
    return _RATE_LIMITER


def _should_retry_exception(exc: BaseException) -> bool:
    if isinstance(exc, httpx.TransportError):
        return True
    if isinstance(exc, RetryableSubstackError):
        return exc.response.status_code in _RETRYABLE_STATUS_CODES
    return False


def _build_before_sleep(
    request_id: str, method: str, url: str
) -> Callable[[RetryCallState], None]:
    def _before_sleep(retry_state: RetryCallState) -> None:
        exc = retry_state.outcome.exception() if retry_state.outcome else None
        elapsed = retry_state.seconds_since_start or 0.0
        next_action = retry_state.next_action
        delay = next_action.sleep if next_action is not None else 0.0
        if isinstance(exc, httpx.TransportError):
            _log.warning(
                "%sSubstack network error: %s %s — %s (%.3fs), retrying in %.3fs",
                request_id,
                method,
                url,
                exc,
                elapsed,
                delay,
            )
        elif isinstance(exc, RetryableSubstackError):
            _log.warning(
                "%s← %s %s → %d (%.3fs), retrying in %.3fs",
                request_id,
                method,
                url,
                exc.response.status_code,
                elapsed,
                delay,
            )

    return _before_sleep


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
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(settings.substack_retry_attempts),
            wait=wait_exponential(
                min=settings.substack_retry_min_wait_sec,
                max=settings.substack_retry_max_wait_sec,
            ),
            retry=retry_if_exception(_should_retry_exception),
            before_sleep=_build_before_sleep(self._rid, method, url),
            sleep=_sleep,
            reraise=True,
        ):
            with attempt:
                limiter = _get_rate_limiter()
                acquired = limiter.try_acquire("substack_api", blocking=True)
                if inspect.isawaitable(acquired):
                    await acquired

                attempt_number = attempt.retry_state.attempt_number
                _log.debug(
                    "%s→ %s %s (attempt %d/%d)",
                    self._rid,
                    method,
                    url,
                    attempt_number,
                    settings.substack_retry_attempts,
                )
                start = time.monotonic()
                try:
                    response = await self._http.request(method, url, **kwargs)
                except httpx.TransportError as exc:
                    elapsed = time.monotonic() - start
                    if attempt_number >= settings.substack_retry_attempts:
                        _log.warning(
                            "%sSubstack network error: %s %s — %s (%.3fs)",
                            self._rid,
                            method,
                            url,
                            exc,
                            elapsed,
                        )
                        raise SubstackAPIError(502, f"Network error: {exc}") from exc
                    raise

                elapsed = time.monotonic() - start
                if response.status_code == 401:
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
                if response.status_code == 403:
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
                if response.status_code in _RETRYABLE_STATUS_CODES:
                    if attempt_number >= settings.substack_retry_attempts:
                        self._raise_api_error(method, url, response, elapsed)
                    raise RetryableSubstackError(response)
                if not response.is_success:
                    self._raise_api_error(method, url, response, elapsed)
                _log.debug(
                    "%s← %s %s → %d (%.3fs)",
                    self._rid,
                    method,
                    url,
                    response.status_code,
                    elapsed,
                )
                return response

        raise RuntimeError("Request retry loop exited unexpectedly")

    def _raise_api_error(
        self, method: str, url: str, response: httpx.Response, elapsed: float
    ) -> None:
        _log.warning(
            "%s← %s %s → %d (%.3fs)",
            self._rid,
            method,
            url,
            response.status_code,
            elapsed,
        )
        try:
            body = response.json()
            detail = (
                body.get("error")
                or body.get("message")
                or f"HTTP {response.status_code}"
            )
        except Exception:
            detail = f"HTTP {response.status_code}"
        raise SubstackAPIError(
            response.status_code,
            f"Substack returned {response.status_code}: {detail}",
        )
