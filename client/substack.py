from __future__ import annotations

from typing import Any

import httpx

from client.exceptions import SubstackAPIError, SubstackAuthError
from models.substack import (
    HandleOptionsResponse,
    SubstackComment,
    SubstackCommentsResponse,
    SubstackFollowingUser,
    SubstackFullPost,
    SubstackItemResponse,
    SubstackNote,
    SubstackNotesPage,
    SubstackProfilePostsPage,
    SubstackPublicProfile,
    SubstackSubscriberLists,
)

_SUBSTACK_BASE = "https://substack.com"
_API_PREFIX = "api/v1"
_TIMEOUT = 10.0
_HOME_TAB_PAYLOAD = {"type": "last_home_tab", "value_text": "inbox"}


class SubstackClient:
    def __init__(self, token: str, publication_url: str) -> None:
        self._cookies = {"connect.sid": token}
        self._pub_base = f"{publication_url.rstrip('/')}/{_API_PREFIX}"
        self._http: httpx.AsyncClient | None = None

    async def __aenter__(self) -> SubstackClient:
        self._http = httpx.AsyncClient(cookies=self._cookies, timeout=_TIMEOUT)
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None

    # ------------------------------------------------------------------
    # Connectivity
    # ------------------------------------------------------------------

    async def check_connectivity(self) -> bool:
        """Mirrors ConnectivityService.isConnected() — never raises."""
        url = f"{self._pub_base}/user-setting"
        try:
            await self._request("PUT", url, json=_HOME_TAB_PAYLOAD)
            return True
        except (SubstackAuthError, SubstackAPIError):
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
        if not response.potentialHandles:
            raise SubstackAPIError(
                502, "Substack returned no potential handles for this account"
            )
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

    async def get_own_following(self) -> list[SubstackFollowingUser]:
        """Mirrors FollowingService.getFollowing() — PUT /user-setting then GET /user/{id}/subscriber-lists."""
        user_id = await self._get_own_id()
        url = f"{self._pub_base}/user/{user_id}/subscriber-lists"
        r = await self._request("GET", url, params={"lists": "following"})
        data = SubstackSubscriberLists.model_validate(r.json())
        users: list[SubstackFollowingUser] = []
        for sl in data.subscriberLists:
            for group in sl.groups:
                users.extend(group.users)
        return users

    async def _get_own_id(self) -> int:
        """Mirrors FollowingService.getOwnId() — PUT /user-setting returns user_id."""
        url = f"{self._pub_base}/user-setting"
        r = await self._request("PUT", url, json=_HOME_TAB_PAYLOAD)
        raw = r.json().get("user_id")
        if raw is None:
            raise SubstackAPIError(502, "Substack response missing user_id field")
        try:
            return int(raw)
        except (TypeError, ValueError) as exc:
            raise SubstackAPIError(
                502, f"Substack returned non-integer user_id: {raw!r}"
            ) from exc

    async def _get_reader_comment(self, comment_id: int) -> SubstackNote:
        """Internal: GET /reader/comment/{id} (global)."""
        url = f"{_SUBSTACK_BASE}/{_API_PREFIX}/reader/comment/{comment_id}"
        r = await self._request("GET", url)
        return SubstackItemResponse.model_validate(r.json()).item

    async def get_note_by_id(self, note_id: int) -> SubstackNote:
        """Mirrors NoteService.getNoteById() — GET /reader/comment/{id} (global)."""
        return await self._get_reader_comment(note_id)

    async def get_comment_by_id(self, comment_id: int) -> SubstackNote:
        """Mirrors CommentService.getCommentById() — GET /reader/comment/{id} (global)."""
        return await self._get_reader_comment(comment_id)

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

    async def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        if self._http is None:
            raise RuntimeError(
                "SubstackClient must be used as an async context manager"
            )
        try:
            r = await self._http.request(method, url, **kwargs)
        except httpx.HTTPError as exc:
            raise SubstackAPIError(502, f"Network error: {exc}") from exc

        if r.status_code == 401:
            raise SubstackAuthError(401, "Invalid or expired Substack session token")
        if r.status_code == 403:
            raise SubstackAuthError(
                403, "Forbidden: insufficient permissions for this resource"
            )
        if not r.is_success:
            raise SubstackAPIError(r.status_code, f"Substack returned {r.status_code}")
        return r
