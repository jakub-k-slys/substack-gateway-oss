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
from gateway_posts.schemas import (  # noqa: F401
    FullPostResponse,
    PostResponse,
    PostsPageResponse,
)
from gateway_profiles.schemas import ProfileResponse  # noqa: F401


class LivenessResponse(BaseModel):
    status: str


TokensInfo = BearerCredentials


class HealthResponse(BaseModel):
    connected: bool
    tokens: TokensInfo | None = None
