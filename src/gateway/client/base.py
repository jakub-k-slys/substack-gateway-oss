from __future__ import annotations

import logging
import time
from typing import Any

import httpx
from typing_extensions import Self

from gateway.client.exceptions import SubstackAPIError, SubstackAuthError
from gateway.config import settings

_log = logging.getLogger(__name__)

_TIMEOUT = settings.substack_timeout
_LIMITS = httpx.Limits(max_connections=20, max_keepalive_connections=5)


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
        _log.debug("%s→ %s %s", self._rid, method, url)
        start = time.monotonic()
        try:
            r = await self._http.request(method, url, **kwargs)
        except httpx.HTTPError as exc:
            elapsed = time.monotonic() - start
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
                "%s← %s %s → 401 Unauthorized (%.3fs)", self._rid, method, url, elapsed
            )
            raise SubstackAuthError(401, "Invalid or expired Substack session token")
        if r.status_code == 403:
            _log.warning(
                "%s← %s %s → 403 Forbidden (%.3fs)", self._rid, method, url, elapsed
            )
            raise SubstackAuthError(
                403, "Forbidden: insufficient permissions for this resource"
            )
        if not r.is_success:
            _log.warning(
                "%s← %s %s → %d (%.3fs)", self._rid, method, url, r.status_code, elapsed
            )
            try:
                body = r.json()
                detail = (
                    body.get("error") or body.get("message") or f"HTTP {r.status_code}"
                )
            except Exception:
                detail = f"HTTP {r.status_code}"
            raise SubstackAPIError(
                r.status_code, f"Substack returned {r.status_code}: {detail}"
            )
        _log.debug(
            "%s← %s %s → %d (%.3fs)", self._rid, method, url, r.status_code, elapsed
        )
        return r
