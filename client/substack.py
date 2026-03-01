from __future__ import annotations

import logging
import time
from typing import Any

import httpx
import pydantic
from async_lru import alru_cache

from client.exceptions import SubstackAPIError, SubstackAuthError
from config import settings
from converters.markdown import markdown_to_note_payload
from models.substack import (
    HandleOptionsResponse,
    SubstackAttachmentCreated,
    SubstackComment,
    SubstackCommentsResponse,
    SubstackDraftByline,
    SubstackDraftCreated,
    SubstackDraftPayload,
    SubstackFollowingUser,
    SubstackFullPost,
    SubstackItemResponse,
    SubstackNote,
    SubstackNoteCreated,
    SubstackNotesPage,
    SubstackPostResponse,
    SubstackProfilePostsPage,
    SubstackPublicProfile,
    SubstackSubscriberLists,
)

_log = logging.getLogger(__name__)

_SUBSTACK_BASE = settings.substack_base_url
_API_PREFIX = "api/v1"
_TIMEOUT = settings.substack_timeout
_LIMITS = httpx.Limits(max_connections=20, max_keepalive_connections=5)
_HOME_TAB_PAYLOAD = {"type": "last_home_tab", "value_text": "inbox"}


class SubstackClient:
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
        # Instance-scoped cache: alru_cache wraps the bound method so the
        # cache key is just (slug,) and the cache lives on this instance.
        # It is GC'd with the client — no cross-request contamination.
        self.get_profile_by_slug = alru_cache(self._fetch_profile)

    async def __aenter__(self) -> SubstackClient:
        self._http = httpx.AsyncClient(
            cookies=self._cookies, timeout=_TIMEOUT, limits=_LIMITS
        )
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None

    # ------------------------------------------------------------------
    # Connectivity
    # ------------------------------------------------------------------

    async def check_connectivity(self) -> bool:
        """GET /feed/following — never raises.

        Returns True when Substack responds (even with an auth error), and
        False only when there is a network-level failure or a server error,
        since those indicate the service itself is unreachable.
        """
        url = f"{self._sub_base}/feed/following"
        _log.debug("Checking connectivity via %s", url)
        try:
            await self._request("GET", url)
            _log.debug("Connectivity check: reachable (authenticated)")
            return True
        except SubstackAuthError:
            # Substack replied — the service is reachable, the token is just invalid.
            _log.debug("Connectivity check: reachable (auth error — token invalid)")
            return True
        except SubstackAPIError:
            _log.warning("Connectivity check: unreachable (API/network error)")
            return False

    # ------------------------------------------------------------------
    # Profile
    # ------------------------------------------------------------------

    async def get_own_profile(self) -> SubstackPublicProfile:
        """Mirrors OwnProfile — fetches handle then full profile."""
        _log.debug("Fetching own profile")
        slug = await self._get_own_slug()
        _log.debug("Resolved own slug: %r", slug)
        return await self.get_profile_by_slug(slug)

    async def _get_own_slug(self) -> str:
        """Mirrors ProfileService.getOwnSlug() — GET /handle/options."""
        _log.debug("Resolving own handle slug via /handle/options")
        url = f"{self._sub_base}/handle/options"
        r = await self._request("GET", url)
        response = HandleOptionsResponse.model_validate(r.json())
        if not response.potential_handles:
            raise SubstackAPIError(
                502, "Substack returned no potential handles for this account"
            )
        return response.potential_handles[0].handle

    async def _fetch_profile(self, slug: str) -> SubstackPublicProfile:
        """GET /user/{slug}/public_profile — called through self.get_profile_by_slug.

        get_profile_by_slug is an alru_cache-wrapped version of this method,
        created per-instance in __init__ so the cache is request-scoped and
        GC'd with the client.
        """
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

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    async def get_own_notes(self, cursor: str | None = None) -> SubstackNotesPage:
        """Mirrors OwnProfile.notes() — GET /notes with optional cursor."""
        _log.debug("Fetching own notes (cursor=%r)", cursor)
        url = f"{self._pub_base}/notes"
        params = {"cursor": cursor} if cursor else {}
        r = await self._request("GET", url, params=params)
        page = SubstackNotesPage.model_validate(r.json())
        _log.debug(
            "Got %d own notes (next_cursor=%r)", len(page.items), page.next_cursor
        )
        return page

    # ------------------------------------------------------------------
    # Posts
    # ------------------------------------------------------------------

    async def get_own_posts(
        self, limit: int = 25, offset: int = 0
    ) -> SubstackProfilePostsPage:
        """Mirrors Profile.posts() — resolves own slug then GET /profile/posts.

        Uses get_profile_id_by_slug instead of get_own_profile to avoid
        constructing the full profile model when only the ID is needed.
        """
        _log.debug("Fetching own posts (limit=%d, offset=%d)", limit, offset)
        slug = await self._get_own_slug()
        profile_id = await self.get_profile_id_by_slug(slug)
        return await self.get_posts_for_profile(profile_id, limit=limit, offset=offset)

    async def get_posts_for_profile(
        self, profile_id: int, limit: int = 25, offset: int = 0
    ) -> SubstackProfilePostsPage:
        """Mirrors PostService.getPostsForProfile() — GET /profile/posts (global)."""
        _log.debug(
            "Fetching posts for profile_id=%d (limit=%d, offset=%d)",
            profile_id,
            limit,
            offset,
        )
        url = f"{self._sub_base}/profile/posts"
        params = {"profile_user_id": profile_id, "limit": limit, "offset": offset}
        r = await self._request("GET", url, params=params)
        page = SubstackProfilePostsPage.model_validate(r.json())
        _log.debug(
            "Got %d posts for profile_id=%d (next_cursor=%r)",
            len(page.posts),
            profile_id,
            page.next_cursor,
        )
        return page

    async def get_notes_for_profile(
        self, profile_id: int, cursor: str | None = None
    ) -> SubstackNotesPage:
        """Mirrors NoteService.getNotesForProfile() — GET /reader/feed/profile/{id}?types=note (pub)."""
        _log.debug("Fetching notes for profile_id=%d (cursor=%r)", profile_id, cursor)
        url = f"{self._pub_base}/reader/feed/profile/{profile_id}"
        params: dict[str, str] = {"types": "note"}
        if cursor:
            params["cursor"] = cursor
        r = await self._request("GET", url, params=params)
        page = SubstackNotesPage.model_validate(r.json())
        _log.debug(
            "Got %d notes for profile_id=%d (next_cursor=%r)",
            len(page.items),
            profile_id,
            page.next_cursor,
        )
        return page

    async def get_own_following(self) -> list[SubstackFollowingUser]:
        """Mirrors FollowingService.getFollowing() — PUT /user-setting then GET /user/{id}/subscriber-lists."""
        _log.debug("Fetching own following list")
        user_id = await self._get_own_id()
        url = f"{self._pub_base}/user/{user_id}/subscriber-lists"
        r = await self._request("GET", url, params={"lists": "following"})
        data = SubstackSubscriberLists.model_validate(r.json())
        users: list[SubstackFollowingUser] = []
        for sl in data.subscriber_lists:
            for group in sl.groups:
                users.extend(group.users)
        _log.debug("Got %d following users for user_id=%d", len(users), user_id)
        return users

    async def _get_own_id(self) -> int:
        """Mirrors FollowingService.getOwnId() — PUT /user-setting returns user_id.

        Note: this is a write operation (it sets the user's last home tab preference
        to "inbox") that Substack's own client uses as the only way to retrieve the
        caller's user ID. There is no read-only alternative in the public API.
        """
        _log.debug("Resolving own user ID via /user-setting")
        url = f"{self._sub_base}/user-setting"
        r = await self._request("PUT", url, json=_HOME_TAB_PAYLOAD)
        raw = r.json().get("user_id")
        if raw is None:
            raise SubstackAPIError(502, "Substack response missing user_id field")
        try:
            user_id = int(raw)
        except (TypeError, ValueError) as exc:
            raise SubstackAPIError(
                502, f"Substack returned non-integer user_id: {raw!r}"
            ) from exc
        _log.debug("Resolved own user_id=%d", user_id)
        return user_id

    async def _get_reader_comment(self, comment_id: int) -> SubstackNote:
        """Internal: GET /reader/comment/{id} (pub)."""
        url = f"{self._pub_base}/reader/comment/{comment_id}"
        r = await self._request("GET", url)
        return SubstackItemResponse.model_validate(r.json()).item

    async def get_note_by_id(self, note_id: int) -> SubstackNote:
        """Mirrors NoteService.getNoteById() — GET /reader/comment/{id} (pub)."""
        _log.debug("Fetching note id=%d", note_id)
        return await self._get_reader_comment(note_id)

    async def get_comment_by_id(self, comment_id: int) -> SubstackNote:
        """Mirrors CommentService.getCommentById() — GET /reader/comment/{id} (pub)."""
        _log.debug("Fetching comment id=%d", comment_id)
        return await self._get_reader_comment(comment_id)

    async def get_post_by_id(self, post_id: int) -> SubstackFullPost:
        """Mirrors PostService.getPostById() — GET /posts/by-id/{id} (global)."""
        _log.debug("Fetching post id=%d", post_id)
        url = f"{self._sub_base}/posts/by-id/{post_id}"
        r = await self._request("GET", url)
        return SubstackPostResponse.model_validate(r.json()).post

    async def get_comments_for_post(self, post_id: int) -> list[SubstackComment]:
        """Mirrors CommentService.getCommentsForPost() — GET /post/{id}/comments (pub)."""
        _log.debug("Fetching comments for post id=%d", post_id)
        url = f"{self._pub_base}/post/{post_id}/comments"
        r = await self._request("GET", url)
        comments = SubstackCommentsResponse.model_validate(r.json()).comments
        _log.debug("Got %d comments for post id=%d", len(comments), post_id)
        return comments

    async def create_attachment(self, url: str) -> SubstackAttachmentCreated:
        """POST /comment/attachment/ to register a link attachment, returns its UUID."""
        _log.debug("Creating attachment for url=%r", url)
        endpoint = f"{self._sub_base}/comment/attachment/"
        r = await self._request("POST", endpoint, json={"url": url, "type": "link"})
        attachment = SubstackAttachmentCreated.model_validate(r.json())
        _log.debug("Created attachment id=%r", attachment.id)
        return attachment

    async def create_note(
        self, content: str, attachment: str | None = None
    ) -> SubstackNoteCreated:
        """Convert markdown to Substack note payload and POST to /comment/feed/."""
        _log.debug("Creating note (%d chars of markdown)", len(content))
        attachment_ids: list[str] | None = None
        if attachment:
            att = await self.create_attachment(attachment)
            attachment_ids = [att.id]
        payload = markdown_to_note_payload(content, attachment_ids=attachment_ids)
        url = f"{self._sub_base}/comment/feed/"
        r = await self._request("POST", url, json=payload)
        note = SubstackNoteCreated.model_validate(r.json())
        _log.debug("Created note id=%d", note.id)
        return note

    async def create_draft(
        self,
        title: str | None = None,
        subtitle: str | None = None,
        body: str | None = None,
    ) -> SubstackDraftCreated:
        """POST /post on the publication to create a new draft."""
        _log.debug("Creating draft title=%r", title)
        user_id = await self._get_own_id()
        payload = SubstackDraftPayload(
            draft_title=title or "",
            draft_subtitle=subtitle or "",
            draft_body=body or "",
            draft_bylines=[SubstackDraftByline(id=user_id)],
        )
        url = f"{self._pub_base}/drafts"
        r = await self._request("POST", url, json=payload.model_dump())
        draft = SubstackDraftCreated.model_validate(r.json())
        _log.debug("Created draft id=%d uuid=%s", draft.id, draft.uuid)
        return draft

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

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
