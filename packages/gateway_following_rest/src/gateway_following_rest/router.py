from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from gateway_following.schemas import FollowingResponse
from gateway_following.service import FollowingService
from gateway_following_rest.deps import get_following_service

router = APIRouter(tags=["following"])


@router.get("/me/following", response_model=FollowingResponse)
async def get_me_following(
    service: Annotated[FollowingService, Depends(get_following_service)],
) -> FollowingResponse:
    """Return the list of users the authenticated user follows."""
    users = await service.get_own_following()
    return FollowingResponse.from_substack(users)
