from __future__ import annotations

import logging

import pydantic
from async_lru import alru_cache

from gateway.client.base import SubstackHTTPBase
from gateway.client.exceptions import SubstackAPIError
from gateway.models.substack import (
    SubstackNotesPage,
    SubstackProfilePostsPage,
    SubstackPublicProfile,
)

_log = logging.getLogger(__name__)


class ProfilesMixin(SubstackHTTPBase):
    def __init__(
        self,
        substack_sid: str,
        connect_sid: str,
        publication_url: str,
        request_id: str | None = None,
    ) -> None:
        super().__init__(substack_sid, connect_sid, publication_url, request_id)
        # Instance-scoped cache: GC'd with the client — no cross-request contamination.
        self.get_profile_by_slug = alru_cache(self._fetch_profile)

    async def get_own_profile(self) -> SubstackPublicProfile:
        """Fetch the authenticated user's own public profile."""
        _log.debug("Fetching own profile")
        slug = await self._get_own_slug()
        _log.debug("Resolved own slug: %r", slug)
        return await self.get_profile_by_slug(slug)

    async def _fetch_profile(self, slug: str) -> SubstackPublicProfile:
        """GET /user/{slug}/public_profile — backing function for get_profile_by_slug cache."""
        _log.debug("Fetching public profile for slug=%r", slug)
        url = f"{self._sub_base}/user/{slug}/public_profile"
        r = await self._request("GET", url)
        try:
            return SubstackPublicProfile.model_validate(r.json())
        except pydantic.ValidationError as exc:
            raise SubstackAPIError(
                502, f"Substack profile response invalid: {exc}"
            ) from exc

    async def get_profile_id_by_slug(self, slug: str) -> int:
        """Return the numeric ID for a profile slug, using the request-scoped cache."""
        profile = await self.get_profile_by_slug(slug)
        return profile.id

    async def get_posts_for_slug(
        self, slug: str, limit: int = 25, offset: int = 0
    ) -> SubstackProfilePostsPage:
        """Resolve slug → profile ID, then fetch posts."""
        profile_id = await self.get_profile_id_by_slug(slug)
        return await self.get_posts_for_profile(profile_id, limit=limit, offset=offset)  # type: ignore[attr-defined]

    async def get_notes_for_slug(
        self, slug: str, cursor: str | None = None
    ) -> SubstackNotesPage:
        """Resolve slug → profile ID, then fetch notes."""
        profile_id = await self.get_profile_id_by_slug(slug)
        return await self.get_notes_for_profile(profile_id, cursor=cursor)  # type: ignore[attr-defined]
