from __future__ import annotations

from typing import Any

from gateway_comments.schemas import (
    CommentsResponse,
    PostCommentRepliesResponse,
    PostCommentResponse,
)
from gateway_comments.service import CommentNotFoundError, CommentsService
from gateway_mcp_common.clients import _authenticated_clients


async def get_post_comments(post_id: int, token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        comments = await CommentsService(pub, sub).get_comments_for_post(post_id)
    return CommentsResponse.from_substack(comments).model_dump()


async def create_post_comment(post_id: int, body: str, token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        comment = await CommentsService(pub, sub).create_top_level_comment(
            post_id, body
        )
    return PostCommentResponse.from_substack(comment).model_dump(exclude_none=True)


async def reply_to_post_comment(
    comment_id: int, body: str, token: str
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        try:
            comment = await CommentsService(pub, sub).reply_to_comment(comment_id, body)
        except CommentNotFoundError as exc:
            raise ValueError(str(exc)) from exc
    return PostCommentResponse.from_substack(comment).model_dump(exclude_none=True)


async def get_post_comment(comment_id: int, token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        comment = await CommentsService(pub, sub).get_post_comment(comment_id)
    return PostCommentResponse.from_substack(comment).model_dump(exclude_none=True)


async def delete_post_comment(comment_id: int, token: str) -> str:
    async with _authenticated_clients(token) as (pub, sub):
        await CommentsService(pub, sub).delete_comment(comment_id)
    return f"Comment {comment_id} deleted successfully."


async def list_post_comment_replies(comment_id: int, token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        replies = await CommentsService(pub, sub).list_comment_replies(comment_id)
    return PostCommentRepliesResponse.from_substack(replies).model_dump(
        exclude_none=True
    )


async def like_post_comment(comment_id: int, token: str) -> str:
    async with _authenticated_clients(token) as (pub, sub):
        await CommentsService(pub, sub).like_comment(comment_id)
    return f"Comment {comment_id} liked successfully."


async def unlike_post_comment(comment_id: int, token: str) -> str:
    async with _authenticated_clients(token) as (pub, sub):
        await CommentsService(pub, sub).unlike_comment(comment_id)
    return f"Comment {comment_id} unliked successfully."
