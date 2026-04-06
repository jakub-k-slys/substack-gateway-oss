from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from gateway_oss.api.deps import get_credentials

from gateway_pro.api.deps import get_post_reactions_service
from gateway_pro.services.post_reactions import PostReactionsService

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
