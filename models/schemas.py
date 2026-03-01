from __future__ import annotations

import logging

from pydantic import BaseModel

from models.substack import (
    SubstackComment,
    SubstackFollowingUser,
    SubstackFullPost,
    SubstackNote,
    SubstackNoteCreated,
    SubstackNotesPage,
    SubstackPreviewPost,
    SubstackProfilePostsPage,
    SubstackPublicProfile,
)

_log = logging.getLogger(__name__)


class LivenessResponse(BaseModel):
    status: str


class BearerCredentials(BaseModel):
    substack_sid: str | None = None
    connect_sid: str | None = None
    gateway_key: str | None = None


class HealthResponse(BaseModel):
    connected: bool


class ProfileResponse(BaseModel):
    id: int
    handle: str
    name: str
    url: str
    avatar_url: str
    bio: str | None = None

    @classmethod
    def from_substack(cls, profile: SubstackPublicProfile) -> ProfileResponse:
        return cls(
            id=profile.id,
            handle=profile.handle,
            name=profile.name,
            url=f"https://substack.com/@{profile.handle}",
            avatar_url=profile.photo_url or "",
            bio=profile.bio,
        )


# ------------------------------------------------------------------
# Notes
# ------------------------------------------------------------------


class NoteAuthor(BaseModel):
    id: int
    name: str
    handle: str
    avatar_url: str


class NoteResponse(BaseModel):
    id: int
    body: str
    likes_count: int
    author: NoteAuthor
    published_at: str

    @classmethod
    def from_substack(cls, note: SubstackNote) -> NoteResponse:
        user = note.context.users[0] if note.context.users else None
        comment = note.comment
        if comment is None:
            _log.warning(
                "Note %r has no comment body; returning empty defaults", note.entity_key
            )
        if user is None:
            _log.warning(
                "Note %r has no author; returning empty defaults", note.entity_key
            )
        return cls(
            id=comment.id if comment else 0,
            body=comment.body if comment else "",
            likes_count=comment.reaction_count
            if (comment and comment.reaction_count is not None)
            else 0,
            author=NoteAuthor(
                id=user.id if user else 0,
                name=user.name if user else "",
                handle=user.handle if user else "",
                avatar_url=user.photo_url or "" if user else "",
            ),
            published_at=note.context.timestamp,
        )


class NotesPageResponse(BaseModel):
    items: list[NoteResponse]
    next_cursor: str | None = None

    @classmethod
    def from_substack(cls, page: SubstackNotesPage) -> NotesPageResponse:
        return cls(
            items=[NoteResponse.from_substack(n) for n in page.items],
            next_cursor=page.next_cursor,
        )


# ------------------------------------------------------------------
# Posts
# ------------------------------------------------------------------


class PostResponse(BaseModel):
    id: int
    title: str
    subtitle: str | None = None
    truncated_body: str | None = None
    published_at: str

    @classmethod
    def from_substack(cls, post: SubstackPreviewPost) -> PostResponse:
        return cls(
            id=post.id,
            title=post.title,
            subtitle=post.subtitle,
            truncated_body=post.truncated_body_text,
            published_at=post.post_date,
        )


class PostsPageResponse(BaseModel):
    items: list[PostResponse]
    next_cursor: str | None = None

    @classmethod
    def from_substack(cls, page: SubstackProfilePostsPage) -> PostsPageResponse:
        return cls(
            items=[PostResponse.from_substack(p) for p in page.posts],
            next_cursor=page.next_cursor,
        )


# ------------------------------------------------------------------
# Full post & comments
# ------------------------------------------------------------------


class FullPostResponse(BaseModel):
    id: int
    title: str
    slug: str
    subtitle: str | None = None
    url: str
    published_at: str
    html_body: str | None = None
    truncated_body: str | None = None
    reactions: dict[str, int] | None = None
    restacks: int | None = None
    tags: list[str] | None = None
    cover_image: str | None = None

    @classmethod
    def from_substack(cls, post: SubstackFullPost) -> FullPostResponse:
        return cls(
            id=post.id,
            title=post.title,
            slug=post.slug,
            subtitle=post.subtitle,
            url=post.canonical_url,
            published_at=post.post_date,
            html_body=post.body_html or post.html_body,
            truncated_body=post.truncated_body_text,
            reactions=post.reactions,
            restacks=post.restacks,
            tags=[t.name for t in post.post_tags] if post.post_tags else None,
            cover_image=post.cover_image,
        )


class CommentResponse(BaseModel):
    id: int
    body: str
    is_admin: bool

    @classmethod
    def from_substack(cls, comment: SubstackComment) -> CommentResponse:
        return cls(
            id=comment.id,
            body=comment.body,
            is_admin=comment.author_is_admin or False,
        )


class CommentsResponse(BaseModel):
    items: list[CommentResponse]

    @classmethod
    def from_substack(cls, comments: list[SubstackComment]) -> CommentsResponse:
        return cls(items=[CommentResponse.from_substack(c) for c in comments])


# ------------------------------------------------------------------
# Following
# ------------------------------------------------------------------


class FollowingUserResponse(BaseModel):
    id: int
    handle: str

    @classmethod
    def from_substack(cls, user: SubstackFollowingUser) -> FollowingUserResponse:
        return cls(id=user.id, handle=user.handle)


class FollowingResponse(BaseModel):
    items: list[FollowingUserResponse]

    @classmethod
    def from_substack(cls, users: list[SubstackFollowingUser]) -> FollowingResponse:
        return cls(items=[FollowingUserResponse.from_substack(u) for u in users])


# ------------------------------------------------------------------
# Note creation
# ------------------------------------------------------------------


class CreateNoteRequest(BaseModel):
    content: str
    attachment: str | None = None


class CreateNoteResponse(BaseModel):
    id: int

    @classmethod
    def from_substack(cls, note: SubstackNoteCreated) -> CreateNoteResponse:
        return cls(id=note.id)
