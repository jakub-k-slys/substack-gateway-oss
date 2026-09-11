from __future__ import annotations

import logging

import pydantic

from gateway_core.caching import get_value_cache
from gateway_core.client.exceptions import SubstackAPIError
from gateway_core.client.substack import SubstackClient
from gateway_core.models.substack import SubstackPublicProfile

_log = logging.getLogger(__name__)


class ProfilesService:
    def __init__(self, sub: SubstackClient) -> None:
        self._sub = sub

    async def get_profile_by_slug(self, slug: str) -> SubstackPublicProfile:
        """Resolve a slug to its public profile, through the installed cache.

        The key is the slug alone — never the per-request service instance — so a
        cached profile is shared across requests and callers. With no cache
        installed this reaches Substack every time.
        """
        return await get_value_cache().get_or_call(
            f"gateway_profiles:public_profile:{slug}",
            lambda: self._fetch_profile(slug),
        )

    async def get_own_profile(self) -> SubstackPublicProfile:
        """Fetch the authenticated user's own public profile."""
        _log.debug("Fetching own profile")
        slug = await self._sub.get_own_slug()
        _log.debug("Resolved own slug: %r", slug)
        return await self.get_profile_by_slug(slug)

    async def get_profile_id_by_slug(self, slug: str) -> int:
        """Return the numeric ID for a profile slug, using the shared cache."""
        profile = await self.get_profile_by_slug(slug)
        return profile.id

    async def _fetch_profile(self, slug: str) -> SubstackPublicProfile:
        """GET /user/{slug}/public_profile — backing function for the profile cache."""
        _log.debug("Fetching public profile for slug=%r", slug)
        r = await self._sub.get(f"user/{slug}/public_profile")
        try:
            return SubstackPublicProfile.model_validate(r.json())
        except pydantic.ValidationError as exc:
            raise SubstackAPIError(
                502, f"Substack profile response invalid: {exc}"
            ) from exc
