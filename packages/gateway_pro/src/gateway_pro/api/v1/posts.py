from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from gateway_oss.api.deps import get_credentials

from gateway_pro.api.deps import get_post_reactions_service, get_post_restacks_service
from gateway_pro.services.post_reactions import PostReactionsService
from gateway_pro.services.post_restacks import PostRestacksService

router = APIRouter(tags=["posts"])


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
