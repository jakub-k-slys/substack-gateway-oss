from __future__ import annotations

import logging

import pydantic
from async_lru import alru_cache

from gateway_oss.client.exceptions import SubstackAPIError
from gateway_oss.client.substack import SubstackClient
from gateway_oss.models.substack import SubstackPublicProfile

_log = logging.getLogger(__name__)


class ProfilesService:
    def __init__(self, sub: SubstackClient) -> None:
        self._sub = sub
        # Instance-scoped cache: GC'd with the service — no cross-request contamination.
        self.get_profile_by_slug = alru_cache(self._fetch_profile)

    async def get_own_profile(self) -> SubstackPublicProfile:
        """Fetch the authenticated user's own public profile."""
        _log.debug("Fetching own profile")
        slug = await self._sub.get_own_slug()
        _log.debug("Resolved own slug: %r", slug)
        return await self.get_profile_by_slug(slug)

    async def get_profile_id_by_slug(self, slug: str) -> int:
        """Return the numeric ID for a profile slug, using the request-scoped cache."""
        profile = await self.get_profile_by_slug(slug)
        return profile.id

    async def _fetch_profile(self, slug: str) -> SubstackPublicProfile:
        """GET /user/{slug}/public_profile — backing function for get_profile_by_slug cache."""
        _log.debug("Fetching public profile for slug=%r", slug)
        r = await self._sub.get(f"user/{slug}/public_profile")
        try:
            return SubstackPublicProfile.model_validate(r.json())
        except pydantic.ValidationError as exc:
            raise SubstackAPIError(
                502, f"Substack profile response invalid: {exc}"
            ) from exc
