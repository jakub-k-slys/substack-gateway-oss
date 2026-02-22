from __future__ import annotations

import httpx

from client.exceptions import SubstackAPIError, SubstackAuthError
from models.substack import HandleOptionsResponse, SubstackPublicProfile

_SUBSTACK_BASE = "https://substack.com"
_API_PREFIX = "api/v1"
_TIMEOUT = 10.0


class SubstackClient:
    def __init__(self, token: str, publication_url: str) -> None:
        self._cookies = {"connect.sid": token}
        self._pub_base = f"{publication_url.rstrip('/')}/{_API_PREFIX}"

    # ------------------------------------------------------------------
    # Connectivity
    # ------------------------------------------------------------------

    async def check_connectivity(self) -> bool:
        """Mirrors ConnectivityService.isConnected() — never raises."""
        url = f"{self._pub_base}/user-setting"
        async with httpx.AsyncClient(cookies=self._cookies, timeout=_TIMEOUT) as http:
            try:
                r = await http.put(
                    url,
                    json={"type": "last_home_tab", "value_text": "inbox"},
                )
                return r.status_code == 200
            except httpx.HTTPError:
                return False

    # ------------------------------------------------------------------
    # Profile
    # ------------------------------------------------------------------

    async def get_own_profile(self) -> SubstackPublicProfile:
        """Mirrors OwnProfile — fetches handle then full profile."""
        slug = await self._get_own_slug()
        return await self.get_profile_by_slug(slug)

    async def _get_own_slug(self) -> str:
        """Mirrors ProfileService.getOwnSlug() — GET /handle/options."""
        url = f"{self._pub_base}/handle/options"
        r = await self._request("GET", url)
        response = HandleOptionsResponse.model_validate(r.json())
        return response.potentialHandles[0].handle

    async def get_profile_by_slug(self, slug: str) -> SubstackPublicProfile:
        """Mirrors ProfileService.getProfileBySlug() — GET /user/{slug}/public_profile."""
        url = f"{_SUBSTACK_BASE}/{_API_PREFIX}/user/{slug}/public_profile"
        r = await self._request("GET", url)
        return SubstackPublicProfile.model_validate(r.json())

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient(cookies=self._cookies, timeout=_TIMEOUT) as http:
            try:
                r = await http.request(method, url, **kwargs)
            except httpx.HTTPError as exc:
                raise SubstackAPIError(502, f"Network error: {exc}") from exc

        if r.status_code in (401, 403):
            raise SubstackAuthError("Invalid or expired Substack session token")
        if not r.is_success:
            raise SubstackAPIError(r.status_code, f"Substack returned {r.status_code}")
        return r
