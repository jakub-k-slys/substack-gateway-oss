from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path

from gateway_oss.api.deps import get_posts_service
from gateway_oss.models.schemas import CommentsResponse
from gateway_oss.services.posts import PostsService

router = APIRouter(tags=["posts"])


@router.get("/posts/{post_id}/comments", response_model=CommentsResponse)
async def get_post_comments(
    post_id: Annotated[int, Path(gt=0)],
    service: Annotated[PostsService, Depends(get_posts_service)],
) -> CommentsResponse:
    """Return comments for the given post."""
    comments = await service.get_comments_for_post(post_id)
    return CommentsResponse.from_substack(comments)
