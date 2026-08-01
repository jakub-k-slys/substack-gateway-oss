from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path

from gateway_comments.schemas import CommentsResponse
from gateway_comments.service import CommentsService
from gateway_comments_rest.deps import get_comments_service
from gateway_notes.schemas import NoteResponse

router = APIRouter(tags=["comments"])


@router.get(
    "/comments/{comment_id}",
    response_model=NoteResponse,
    response_model_exclude_none=True,
)
async def get_comment(
    comment_id: Annotated[int, Path(gt=0)],
    service: Annotated[CommentsService, Depends(get_comments_service)],
) -> NoteResponse:
    """Return a single Substack comment by its ID (reader comment wire format)."""
    comment = await service.get_comment_by_id(comment_id)
    return NoteResponse.from_substack(comment)


@router.get("/posts/{post_id}/comments", response_model=CommentsResponse)
async def get_post_comments(
    post_id: Annotated[int, Path(gt=0)],
    service: Annotated[CommentsService, Depends(get_comments_service)],
) -> CommentsResponse:
    """Return comments for the given post."""
    comments = await service.get_comments_for_post(post_id)
    return CommentsResponse.from_substack(comments)
