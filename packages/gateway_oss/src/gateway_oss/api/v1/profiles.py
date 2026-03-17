from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from gateway_oss.api.deps import get_posts_service, get_profiles_service
from gateway_oss.models.pagination import CursorPage, OffsetPage
from gateway_oss.models.schemas import (
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)
from gateway_oss.services.posts import PostsService
from gateway_oss.services.profiles import ProfilesService

router = APIRouter(tags=["profiles"])


@router.get("/profiles/{slug}", response_model=ProfileResponse)
async def get_profile(
    slug: str,
    service: Annotated[ProfilesService, Depends(get_profiles_service)],
) -> ProfileResponse:
    """Return a Substack user's public profile by their handle slug."""
    profile = await service.get_profile_by_slug(slug)
    return ProfileResponse.from_substack(profile)


@router.get("/profiles/{slug}/posts", response_model=PostsPageResponse)
async def get_profile_posts(
    slug: str,
    profiles: Annotated[ProfilesService, Depends(get_profiles_service)],
    posts: Annotated[PostsService, Depends(get_posts_service)],
    page: Annotated[OffsetPage, Depends()],
) -> PostsPageResponse:
    """Return a page of posts for the given profile slug."""
    profile_id = await profiles.get_profile_id_by_slug(slug)
    result = await posts.get_posts_for_profile(
        profile_id, limit=page.limit, offset=page.offset
    )
    return PostsPageResponse.from_substack(result)


@router.get("/profiles/{slug}/notes", response_model=NotesPageResponse)
async def get_profile_notes(
    slug: str,
    profiles: Annotated[ProfilesService, Depends(get_profiles_service)],
    posts: Annotated[PostsService, Depends(get_posts_service)],
    page: Annotated[CursorPage, Depends()],
) -> NotesPageResponse:
    """Return a page of notes for the given profile slug."""
    profile_id = await profiles.get_profile_id_by_slug(slug)
    result = await posts.get_notes_for_profile(profile_id, cursor=page.cursor)
    return NotesPageResponse.from_substack(result)
