from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from gateway.api.deps import (
    get_following_service,
    get_notes_service,
    get_posts_service,
    get_profiles_service,
)
from gateway.models.pagination import CursorPage, OffsetPage
from gateway.models.schemas import (
    FollowingResponse,
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)
from gateway.services.following import FollowingService
from gateway.services.notes import NotesService
from gateway.services.posts import PostsService
from gateway.services.profiles import ProfilesService

router = APIRouter(tags=["me"])


@router.get("/me", response_model=ProfileResponse)
async def get_me(
    service: Annotated[ProfilesService, Depends(get_profiles_service)],
) -> ProfileResponse:
    """Return the authenticated user's own Substack profile."""
    profile = await service.get_own_profile()
    return ProfileResponse.from_substack(profile)


@router.get("/me/notes", response_model=NotesPageResponse)
async def get_me_notes(
    service: Annotated[NotesService, Depends(get_notes_service)],
    page: Annotated[CursorPage, Depends()],
) -> NotesPageResponse:
    """Return a page of the authenticated user's own notes."""
    result = await service.get_own_notes(cursor=page.cursor)
    return NotesPageResponse.from_substack(result)


@router.get("/me/posts", response_model=PostsPageResponse)
async def get_me_posts(
    profiles: Annotated[ProfilesService, Depends(get_profiles_service)],
    posts: Annotated[PostsService, Depends(get_posts_service)],
    page: Annotated[OffsetPage, Depends()],
) -> PostsPageResponse:
    """Return a page of the authenticated user's own posts."""
    profile = await profiles.get_own_profile()
    result = await posts.get_posts_for_profile(
        profile.id, limit=page.limit, offset=page.offset
    )
    return PostsPageResponse.from_substack(result)


@router.get("/me/following", response_model=FollowingResponse)
async def get_me_following(
    service: Annotated[FollowingService, Depends(get_following_service)],
) -> FollowingResponse:
    """Return the list of users the authenticated user follows."""
    users = await service.get_own_following()
    return FollowingResponse.from_substack(users)
