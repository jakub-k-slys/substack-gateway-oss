from __future__ import annotations

import logging
import time
from typing import Any

import httpx
from typing_extensions import Self

from gateway.client.exceptions import SubstackAPIError, SubstackAuthError
from gateway.config import settings
from gateway.models.substack import HandleOptionsResponse, SubstackUserSettingsResponse

_log = logging.getLogger(__name__)

_SUBSTACK_BASE = settings.substack_base_url
_API_PREFIX = "api/v1"
_TIMEOUT = settings.substack_timeout
_LIMITS = httpx.Limits(max_connections=20, max_keepalive_connections=5)


class SubstackHTTPBase:
    """Raw HTTP layer shared by all service mixins."""

    def __init__(
        self,
        substack_sid: str,
        connect_sid: str,
        publication_url: str,
        request_id: str | None = None,
    ) -> None:
        self._cookies = {"substack.sid": substack_sid, "connect.sid": connect_sid}
        self._pub_base = f"{publication_url.rstrip('/')}/{_API_PREFIX}"
        self._sub_base = f"{_SUBSTACK_BASE}/{_API_PREFIX}"
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

    async def check_connectivity(self) -> bool:
        """GET /feed/following — never raises; returns False only on network failure."""
        url = f"{self._sub_base}/feed/following"
        _log.debug("Checking connectivity via %s", url)
        try:
            await self._request("GET", url)
            _log.debug("Connectivity check: reachable (authenticated)")
            return True
        except SubstackAuthError:
            _log.debug("Connectivity check: reachable (auth error — token invalid)")
            return True
        except SubstackAPIError:
            _log.warning("Connectivity check: unreachable (API/network error)")
            return False

    async def get_own_slug(self) -> str:
        """GET /handle/options — resolves the caller's own handle slug."""
        _log.debug("Resolving own handle slug via /handle/options")
        url = f"{self._sub_base}/handle/options"
        r = await self._request("GET", url)
        response = HandleOptionsResponse.model_validate(r.json())
        if not response.potential_handles:
            raise SubstackAPIError(
                502, "Substack returned no potential handles for this account"
            )
        return response.potential_handles[0].handle

    async def get_own_id(self) -> int:
        """GET /user-settings — resolves the caller's own numeric user ID."""
        _log.debug("Resolving own user ID via /user-settings")
        url = f"{self._sub_base}/user-settings"
        r = await self._request("GET", url)
        response = SubstackUserSettingsResponse.model_validate(r.json())
        if not response.user_settings:
            raise SubstackAPIError(502, "Substack returned no user settings")
        user_id = response.user_settings[0].user_id
        _log.debug("Resolved own user_id=%d", user_id)
        return user_id

    async def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        if self._http is None:
            raise RuntimeError(
                "SubstackClient must be used as an async context manager"
            )
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
