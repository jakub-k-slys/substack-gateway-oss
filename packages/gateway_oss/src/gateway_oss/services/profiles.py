from __future__ import annotations

import logging

import pydantic
from aiocache import cached_stampede

from gateway_oss.client.exceptions import SubstackAPIError
from gateway_oss.client.substack import SubstackClient
from gateway_oss.config import settings
from gateway_oss.models.substack import SubstackPublicProfile

_log = logging.getLogger(__name__)


def _build_profile_cache_key(func, _profiles: ProfilesService, slug: str) -> str:
    # Key on the slug only — never on the (per-request) service instance, so the
    # public profile is shared across requests and callers.
    return ":".join((func.__module__, func.__qualname__, slug))


@cached_stampede(
    alias="default",
    ttl=settings.profile_cache_ttl_sec,
    lease=2,
    key_builder=_build_profile_cache_key,
)
async def _get_cached_profile(
    profiles: ProfilesService, slug: str
) -> SubstackPublicProfile:
    """Resolve a public profile by slug via the shared cache.

    Module-level (not an instance method) so aiocache keys on the slug rather than
    the per-request ``ProfilesService`` instance. Backed by the shared
    ``"default"`` cache, so a slug is resolved against Substack at most once per
    TTL across the whole process — and across replicas when backed by Redis.
    """
    return await profiles._fetch_profile(slug)


class ProfilesService:
    def __init__(self, sub: SubstackClient) -> None:
        self._sub = sub

    async def get_profile_by_slug(self, slug: str) -> SubstackPublicProfile:
        """Resolve a slug to its public profile, cached across requests."""
        return await _get_cached_profile(self, slug)

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
