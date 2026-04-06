from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlencode

import pydantic
from gateway_oss.client.substack import SubstackClient
from gateway_oss.models.substack import (
    SubstackNote,
    SubstackNotesPage,
    SubstackPreviewPost,
)
from gateway_oss.services.profiles import ProfilesService


@dataclass(slots=True)
class AtomFeedAuthor:
    name: str
    handle: str
    avatar_url: str


@dataclass(slots=True)
class AtomFeedEntry:
    entry_id: str
    title: str
    url: str
    published_at: str
    updated_at: str
    summary: str | None
    content_html: str | None
    author: AtomFeedAuthor


@dataclass(slots=True)
class AtomFeedPage:
    feed_id: str
    title: str
    subtitle: str | None
    author: AtomFeedAuthor
    updated_at: str
    icon_url: str | None
    alternate_url: str
    self_url: str
    next_url: str | None
    entries: list[AtomFeedEntry]


class SubstackCursorPostsPage(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    posts: list[SubstackPreviewPost] = []
    next_cursor: str | None = pydantic.Field(alias="nextCursor", default=None)


class ProfileFeedService:
    def __init__(self, sub: SubstackClient) -> None:
        self._sub = sub
        self._profiles = ProfilesService(sub)

    async def get_feed_page(
        self,
        slug: str,
        *,
        feed_type: Literal["mixed", "post", "note"] = "mixed",
        notes_cursor: str | None = None,
        posts_cursor: str | None = None,
        limit: int = 50,
        feed_url: str,
    ) -> AtomFeedPage:
        profile = await self._profiles.get_profile_by_slug(slug)
        notes_page = await self._get_notes_page(
            profile.id,
            feed_type=feed_type,
            cursor=notes_cursor,
        )
        posts_page = await self._get_posts_page(
            profile.id,
            feed_type=feed_type,
            cursor=posts_cursor,
            limit=limit,
        )

        author = AtomFeedAuthor(
            name=profile.name,
            handle=profile.handle,
            avatar_url=profile.photo_url or "",
        )
        entries = await self._build_entries(
            author,
            notes_page,
            posts_page.posts,
            feed_type=feed_type,
        )
        entries.sort(key=lambda entry: entry.updated_at, reverse=True)
        entries = entries[:limit]
        updated_at = (
            entries[0].updated_at if entries else (profile.profile_set_up_at or "")
        )

        return AtomFeedPage(
            feed_id=f"tag:substack-gateway,profile:{profile.id}",
            title=f"{profile.name} on Substack",
            subtitle=profile.bio,
            author=author,
            updated_at=updated_at,
            icon_url=profile.photo_url,
            alternate_url=f"https://substack.com/@{profile.handle}",
            self_url=self._build_feed_url(
                feed_url,
                feed_type=feed_type,
                notes_cursor=notes_cursor,
                posts_cursor=posts_cursor,
                limit=limit,
            ),
            next_url=self._build_next_url(
                feed_url,
                feed_type,
                notes_page.next_cursor,
                posts_page.next_cursor,
                limit,
            ),
            entries=entries,
        )

    async def _build_entries(
        self,
        author: AtomFeedAuthor,
        notes_page: SubstackNotesPage,
        posts: list[SubstackPreviewPost],
        *,
        feed_type: Literal["mixed", "post", "note"],
    ) -> list[AtomFeedEntry]:
        entries: list[AtomFeedEntry] = []
        if feed_type in {"mixed", "note"}:
            entries.extend(
                self._note_to_entry(note, fallback_author=author)
                for note in notes_page.items
            )

        if feed_type in {"mixed", "post"}:
            entries.extend(
                self._post_to_entry(post, fallback_author=author) for post in posts
            )
        return entries

    async def _get_notes_for_profile(
        self, profile_id: int, *, cursor: str | None
    ) -> SubstackNotesPage:
        params: dict[str, str] = {}
        if cursor:
            params["cursor"] = cursor
        response = await self._sub.get(
            f"reader/feed/profile/{profile_id}", params=params
        )
        return SubstackNotesPage.model_validate(response.json())

    async def _get_notes_page(
        self,
        profile_id: int,
        *,
        feed_type: Literal["mixed", "post", "note"],
        cursor: str | None,
    ) -> SubstackNotesPage:
        if feed_type == "post":
            return SubstackNotesPage()
        return await self._get_notes_for_profile(profile_id, cursor=cursor)

    async def _get_posts_for_profile(
        self, profile_id: int, *, cursor: str | None, limit: int
    ) -> SubstackCursorPostsPage:
        params: dict[str, str | int] = {
            "profile_user_id": profile_id,
            "limit": limit,
        }
        if cursor:
            params["next_cursor"] = cursor
        response = await self._sub.get("profile/posts", params=params)
        return SubstackCursorPostsPage.model_validate(response.json())

    async def _get_posts_page(
        self,
        profile_id: int,
        *,
        feed_type: Literal["mixed", "post", "note"],
        cursor: str | None,
        limit: int,
    ) -> SubstackCursorPostsPage:
        if feed_type == "note":
            return SubstackCursorPostsPage()
        return await self._get_posts_for_profile(profile_id, cursor=cursor, limit=limit)

    def _note_to_entry(
        self, note: SubstackNote, *, fallback_author: AtomFeedAuthor
    ) -> AtomFeedEntry:
        user = note.context.users[0] if note.context.users else None
        comment = note.comment
        author = AtomFeedAuthor(
            name=user.name if user else fallback_author.name,
            handle=user.handle if user else fallback_author.handle,
            avatar_url=user.photo_url
            if user and user.photo_url
            else fallback_author.avatar_url,
        )
        note_id = comment.id if comment else note.entity_key
        body = comment.body if comment else ""
        return AtomFeedEntry(
            entry_id=f"tag:substack-gateway,note:{note_id}",
            title=f"Note by {author.name}",
            url=f"https://substack.com/@{author.handle}",
            published_at=note.context.timestamp,
            updated_at=note.context.timestamp,
            summary=body,
            content_html=f"<p>{body}</p>" if body else None,
            author=author,
        )

    def _post_to_entry(
        self, post: SubstackPreviewPost, *, fallback_author: AtomFeedAuthor
    ) -> AtomFeedEntry:
        return AtomFeedEntry(
            entry_id=f"tag:substack-gateway,post:{post.id}",
            title=post.title,
            url=f"https://substack.com/@{fallback_author.handle}",
            published_at=post.post_date,
            updated_at=post.post_date,
            summary=post.subtitle or post.truncated_body_text,
            content_html=None,
            author=fallback_author,
        )

    def _build_next_url(
        self,
        feed_url: str,
        feed_type: Literal["mixed", "post", "note"],
        notes_cursor: str | None,
        posts_cursor: str | None,
        limit: int,
    ) -> str | None:
        if notes_cursor is None and posts_cursor is None:
            return None
        return self._build_feed_url(
            feed_url,
            feed_type=feed_type,
            notes_cursor=notes_cursor,
            posts_cursor=posts_cursor,
            limit=limit,
        )

    def _build_feed_url(
        self,
        feed_url: str,
        *,
        feed_type: Literal["mixed", "post", "note"],
        notes_cursor: str | None,
        posts_cursor: str | None,
        limit: int,
    ) -> str:
        query = {
            "limit": str(limit),
            "type": feed_type,
        }
        if notes_cursor:
            query["notes_cursor"] = notes_cursor
        if posts_cursor:
            query["posts_cursor"] = posts_cursor
        encoded = urlencode(query)
        return feed_url if not encoded else f"{feed_url}?{encoded}"
