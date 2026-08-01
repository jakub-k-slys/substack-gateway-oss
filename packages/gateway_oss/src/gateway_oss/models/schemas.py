from __future__ import annotations

from pydantic import BaseModel

from gateway_comments.schemas import CommentResponse, CommentsResponse  # noqa: F401
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
