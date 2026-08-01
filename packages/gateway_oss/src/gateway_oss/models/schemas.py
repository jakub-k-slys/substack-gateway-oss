from __future__ import annotations

from pydantic import BaseModel

from gateway_core.auth import BearerCredentials  # noqa: F401
from gateway_following.schemas import (  # noqa: F401
    FollowingResponse,
    FollowingUserResponse,
)
from gateway_notes.schemas import (  # noqa: F401
    CreateNoteRequest,
    CreateNoteResponse,
    NoteResponse,
    NotesPageResponse,
)
from gateway_oss.converters.markdown import (
    html_to_markdown,
)
from gateway_oss.models.substack import (
    SubstackComment,
    SubstackFullPost,
    SubstackPreviewPost,
    SubstackProfilePostsPage,
    SubstackPublicProfile,
)


class LivenessResponse(BaseModel):
    status: str


TokensInfo = BearerCredentials


class HealthResponse(BaseModel):
    connected: bool
    tokens: TokensInfo | None = None


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
    next: str | None = None

    @classmethod
    def from_substack(cls, page: SubstackProfilePostsPage) -> PostsPageResponse:
        return cls(
            items=[PostResponse.from_substack(p) for p in page.posts],
            next=page.next_cursor,
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
    markdown: str | None = None
    truncated_body: str | None = None
    reactions: dict[str, int] | None = None
    restacks: int | None = None
    tags: list[str] | None = None
    cover_image: str | None = None

    @classmethod
    def from_substack(cls, post: SubstackFullPost) -> FullPostResponse:
        raw_html = post.body_html or post.html_body
        return cls(
            id=post.id,
            title=post.title,
            slug=post.slug,
            subtitle=post.subtitle,
            url=post.canonical_url,
            published_at=post.post_date,
            html_body=raw_html,
            markdown=html_to_markdown(raw_html) if raw_html else None,
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
    author_name: str | None = None
    author_handle: str | None = None
    user_id: int | None = None

    @classmethod
    def from_substack(cls, comment: SubstackComment) -> CommentResponse:
        return cls(
            id=comment.id,
            body=comment.body,
            is_admin=comment.author_is_admin or False,
            author_name=comment.name,
            author_handle=comment.handle,
            user_id=comment.user_id,
        )


class CommentsResponse(BaseModel):
    items: list[CommentResponse]

    @classmethod
    def from_substack(cls, comments: list[SubstackComment]) -> CommentsResponse:
        return cls(items=[CommentResponse.from_substack(c) for c in comments])
