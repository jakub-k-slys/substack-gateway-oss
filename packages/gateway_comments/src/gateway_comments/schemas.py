from __future__ import annotations

from pydantic import BaseModel

from gateway_core.models.substack import SubstackComment


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
