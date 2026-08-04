from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field

from gateway_comments.schemas import (
    CommentsResponse,
    PostCommentRepliesResponse,
    PostCommentResponse,
)
from gateway_comments.service import CommentNotFoundError, CommentsService
from gateway_comments_rest.deps import get_comments_service
from gateway_rest_common.deps import get_credentials

router = APIRouter(tags=["comments"])


class CreateCommentRequest(BaseModel):
    body: str = Field(min_length=1)


@router.post(
    "/posts/{post_id}/comments",
    status_code=201,
    response_model=PostCommentResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(get_credentials)],
)
async def create_post_comment(
    post_id: Annotated[int, Path(gt=0)],
    payload: CreateCommentRequest,
    service: Annotated[CommentsService, Depends(get_comments_service)],
) -> PostCommentResponse:
    comment = await service.create_top_level_comment(post_id, payload.body)
    return PostCommentResponse.from_substack(comment)


@router.post(
    "/comments/{comment_id}/comments",
    status_code=201,
    response_model=PostCommentResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(get_credentials)],
)
async def reply_to_comment(
    comment_id: Annotated[int, Path(gt=0)],
    payload: CreateCommentRequest,
    service: Annotated[CommentsService, Depends(get_comments_service)],
) -> PostCommentResponse:
    try:
        comment = await service.reply_to_comment(comment_id, payload.body)
    except CommentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return PostCommentResponse.from_substack(comment)


@router.get(
    "/comments/{comment_id}",
    response_model=PostCommentResponse,
    response_model_exclude_none=True,
)
async def get_comment(
    comment_id: Annotated[int, Path(gt=0)],
    service: Annotated[CommentsService, Depends(get_comments_service)],
) -> PostCommentResponse:
    """Return a single Substack comment by its ID (rich comment shape)."""
    comment = await service.get_post_comment(comment_id)
    return PostCommentResponse.from_substack(comment)


@router.delete(
    "/comments/{comment_id}",
    status_code=204,
    dependencies=[Depends(get_credentials)],
)
async def delete_comment(
    comment_id: Annotated[int, Path(gt=0)],
    service: Annotated[CommentsService, Depends(get_comments_service)],
) -> None:
    await service.delete_comment(comment_id)


@router.get(
    "/comments/{comment_id}/comments",
    response_model=PostCommentRepliesResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(get_credentials)],
)
async def list_comment_replies(
    comment_id: Annotated[int, Path(gt=0)],
    service: Annotated[CommentsService, Depends(get_comments_service)],
) -> PostCommentRepliesResponse:
    replies = await service.list_comment_replies(comment_id)
    return PostCommentRepliesResponse.from_substack(replies)


@router.post(
    "/comments/{comment_id}/reaction",
    status_code=204,
    dependencies=[Depends(get_credentials)],
)
async def like_comment(
    comment_id: Annotated[int, Path(gt=0)],
    service: Annotated[CommentsService, Depends(get_comments_service)],
) -> None:
    await service.like_comment(comment_id)


@router.delete(
    "/comments/{comment_id}/reaction",
    status_code=204,
    dependencies=[Depends(get_credentials)],
)
async def unlike_comment(
    comment_id: Annotated[int, Path(gt=0)],
    service: Annotated[CommentsService, Depends(get_comments_service)],
) -> None:
    await service.unlike_comment(comment_id)


@router.get("/posts/{post_id}/comments", response_model=CommentsResponse)
async def get_post_comments(
    post_id: Annotated[int, Path(gt=0)],
    service: Annotated[CommentsService, Depends(get_comments_service)],
) -> CommentsResponse:
    """Return comments for the given post."""
    comments = await service.get_comments_for_post(post_id)
    return CommentsResponse.from_substack(comments)
