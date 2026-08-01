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
from gateway_oss.models.substack import (
    SubstackComment,
    SubstackPublicProfile,
)
from gateway_posts.schemas import (  # noqa: F401
    FullPostResponse,
    PostResponse,
    PostsPageResponse,
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
# Comments
# ------------------------------------------------------------------


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
