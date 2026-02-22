from __future__ import annotations

import httpx

from client.exceptions import SubstackAPIError, SubstackAuthError
from models.substack import (
    HandleOptionsResponse,
    SubstackComment,
    SubstackCommentsResponse,
    SubstackFullPost,
    SubstackNotesPage,
    SubstackProfilePostsPage,
    SubstackPublicProfile,
)

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
    # Notes
    # ------------------------------------------------------------------

    async def get_own_notes(self, cursor: str | None = None) -> SubstackNotesPage:
        """Mirrors OwnProfile.notes() — GET /notes with optional cursor."""
        url = f"{self._pub_base}/notes"
        params = {"cursor": cursor} if cursor else {}
        r = await self._request("GET", url, params=params)
        return SubstackNotesPage.model_validate(r.json())

    # ------------------------------------------------------------------
    # Posts
    # ------------------------------------------------------------------

    async def get_own_posts(
        self, limit: int = 25, offset: int = 0
    ) -> SubstackProfilePostsPage:
        """Mirrors Profile.posts() — resolves own ID then GET /profile/posts."""
        profile = await self.get_own_profile()
        return await self.get_posts_for_profile(profile.id, limit=limit, offset=offset)

    async def get_posts_for_profile(
        self, profile_id: int, limit: int = 25, offset: int = 0
    ) -> SubstackProfilePostsPage:
        """Mirrors PostService.getPostsForProfile() — GET /profile/posts (pub)."""
        url = f"{self._pub_base}/profile/posts"
        params = {"profile_user_id": profile_id, "limit": limit, "offset": offset}
        r = await self._request("GET", url, params=params)
        return SubstackProfilePostsPage.model_validate(r.json())

    async def get_notes_for_profile(
        self, profile_id: int, cursor: str | None = None
    ) -> SubstackNotesPage:
        """Mirrors Profile.notes() — GET /reader/feed/profile/{id}?types=note (global)."""
        url = f"{_SUBSTACK_BASE}/{_API_PREFIX}/reader/feed/profile/{profile_id}"
        params: dict[str, str] = {"types": "note"}
        if cursor:
            params["cursor"] = cursor
        r = await self._request("GET", url, params=params)
        return SubstackNotesPage.model_validate(r.json())

    async def get_post_by_id(self, post_id: int) -> SubstackFullPost:
        """Mirrors PostService.getPostById() — GET /posts/by-id/{id} (global)."""
        url = f"{_SUBSTACK_BASE}/{_API_PREFIX}/posts/by-id/{post_id}"
        r = await self._request("GET", url)
        return SubstackFullPost.model_validate(r.json())

    async def get_comments_for_post(self, post_id: int) -> list[SubstackComment]:
        """Mirrors CommentService.getCommentsForPost() — GET /post/{id}/comments (pub)."""
        url = f"{self._pub_base}/post/{post_id}/comments"
        r = await self._request("GET", url)
        return SubstackCommentsResponse.model_validate(r.json()).comments

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
