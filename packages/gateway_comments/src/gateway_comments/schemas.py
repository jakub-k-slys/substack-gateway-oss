from __future__ import annotations

from pydantic import BaseModel

from gateway_core.models.substack import SubstackComment, SubstackPostComment


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


class PostCommentResponse(BaseModel):
    id: int
    body: str
    parent_id: int | None = None
    post_id: int | None = None
    user_id: int | None = None
    date: str | None = None
    deleted: bool = False
    author_name: str | None = None
    reaction_count: int | None = None

    @classmethod
    def from_substack(cls, c: SubstackPostComment) -> PostCommentResponse:
        return cls(
            id=c.id,
            body=c.body,
            parent_id=c.parent_id,
            post_id=c.post_id,
            user_id=c.user_id,
            date=c.date,
            deleted=c.deleted,
            author_name=c.name,
            reaction_count=c.reaction_count,
        )


class PostCommentRepliesResponse(BaseModel):
    items: list[PostCommentResponse]

    @classmethod
    def from_substack(
        cls, replies: list[SubstackPostComment]
    ) -> PostCommentRepliesResponse:
        return cls(items=[PostCommentResponse.from_substack(c) for c in replies])
