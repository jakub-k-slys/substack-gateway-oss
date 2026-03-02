from __future__ import annotations

import logging

from gateway.client.base import SubstackHTTPBase
from gateway.client.exceptions import SubstackAPIError, SubstackAuthError
from gateway.config import settings
from gateway.models.substack import HandleOptionsResponse, SubstackUserSettingsResponse

_log = logging.getLogger(__name__)

_API_PREFIX = "api/v1"


class SubstackClient(SubstackHTTPBase):
    """HTTP client for the global Substack platform API.

    Handles all requests to ``https://substack.com/api/v1/*`` and provides
    helpers for resolving the caller's own identity.  Domain logic lives in
    the service classes (``gateway.services.*``).
    """

    def __init__(
        self,
        substack_sid: str,
        connect_sid: str,
        request_id: str | None = None,
    ) -> None:
        super().__init__(substack_sid, connect_sid, request_id)
        self._base = f"{settings.substack_base_url}/{_API_PREFIX}"

    async def check_connectivity(self) -> bool:
        """GET /feed/following — never raises; returns False only on network failure."""
        _log.debug("Checking connectivity via feed/following")
        try:
            await self.get("feed/following")
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
        r = await self.get("handle/options")
        response = HandleOptionsResponse.model_validate(r.json())
        if not response.potential_handles:
            raise SubstackAPIError(
                502, "Substack returned no potential handles for this account"
            )
        return response.potential_handles[0].handle

    async def get_own_id(self) -> int:
        """GET /user-settings — resolves the caller's own numeric user ID."""
        _log.debug("Resolving own user ID via /user-settings")
        r = await self.get("user-settings")
        response = SubstackUserSettingsResponse.model_validate(r.json())
        if not response.user_settings:
            raise SubstackAPIError(502, "Substack returned no user settings")
        user_id = response.user_settings[0].user_id
        _log.debug("Resolved own user_id=%d", user_id)
        return user_id
