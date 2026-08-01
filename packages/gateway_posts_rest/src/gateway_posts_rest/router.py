from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path

from gateway_posts.schemas import FullPostResponse
from gateway_posts.service import PostsService
from gateway_posts_rest.deps import get_posts_service

router = APIRouter(tags=["posts"])


@router.get("/posts/{post_id}", response_model=FullPostResponse)
async def get_post(
    post_id: Annotated[int, Path(gt=0)],
    service: Annotated[PostsService, Depends(get_posts_service)],
) -> FullPostResponse:
    """Return a single Substack post with its full content."""
    post = await service.get_post_by_id(post_id)
    return FullPostResponse.from_substack(post)
