from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path

from gateway_posts.schemas import FullPostResponse
from gateway_posts.service import (
    PostReactionsService,
    PostRestacksService,
    PostsService,
)
from gateway_posts_rest.deps import (
    get_post_reactions_service,
    get_post_restacks_service,
    get_posts_service,
)
from gateway_rest_common.deps import get_credentials

router = APIRouter(tags=["posts"])


@router.get("/posts/{post_id}", response_model=FullPostResponse)
async def get_post(
    post_id: Annotated[int, Path(gt=0)],
    service: Annotated[PostsService, Depends(get_posts_service)],
) -> FullPostResponse:
    """Return a single Substack post with its full content."""
    post = await service.get_post_by_id(post_id)
    return FullPostResponse.from_substack(post)


@router.put(
    "/posts/{post_id}/like",
    status_code=204,
    dependencies=[Depends(get_credentials)],
)
async def like_post(
    post_id: Annotated[int, Path(gt=0)],
    service: Annotated[PostReactionsService, Depends(get_post_reactions_service)],
) -> None:
    """Add a like to a Substack post."""
    await service.like_post(post_id)


@router.delete(
    "/posts/{post_id}/like",
    status_code=204,
    dependencies=[Depends(get_credentials)],
)
async def unlike_post(
    post_id: Annotated[int, Path(gt=0)],
    service: Annotated[PostReactionsService, Depends(get_post_reactions_service)],
) -> None:
    """Remove a like from a Substack post."""
    await service.unlike_post(post_id)


@router.post(
    "/posts/{post_id}/restack",
    status_code=204,
    dependencies=[Depends(get_credentials)],
)
async def restack_post(
    post_id: Annotated[int, Path(gt=0)],
    service: Annotated[PostRestacksService, Depends(get_post_restacks_service)],
) -> None:
    """Restack a Substack post."""
    await service.restack_post(post_id)
