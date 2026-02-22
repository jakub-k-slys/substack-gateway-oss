from __future__ import annotations

from pydantic import BaseModel

from models.substack import SubstackNote, SubstackPreviewPost, SubstackPublicProfile


class HealthResponse(BaseModel):
    connected: bool


class ProfileResponse(BaseModel):
    id: int
    slug: str
    handle: str
    name: str
    url: str
    avatar_url: str
    bio: str | None = None

    @classmethod
    def from_substack(cls, profile: SubstackPublicProfile) -> ProfileResponse:
        return cls(
            id=profile.id,
            slug=profile.handle,
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
        return cls(
            id=comment.id if comment else 0,
            body=comment.body if comment else "",
            likes_count=comment.reaction_count or 0 if comment else 0,
            author=NoteAuthor(
                id=user.id if user else 0,
                name=user.name if user else "",
                handle=user.handle if user else "",
                avatar_url=user.photo_url if user else "",
            ),
            published_at=note.context.timestamp,
        )


class NotesPageResponse(BaseModel):
    items: list[NoteResponse]
    next_cursor: str | None = None


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


class ErrorResponse(BaseModel):
    error: str
    message: str
    status: int
