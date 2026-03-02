from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from gateway.api.deps import get_substack_client
from gateway.client.substack import SubstackClient
from gateway.models.pagination import CursorPage, OffsetPage
from gateway.models.schemas import (
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)

router = APIRouter(tags=["profiles"])


@router.get("/profiles/{slug}", response_model=ProfileResponse)
async def get_profile(
    slug: str,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> ProfileResponse:
    """Return a Substack user's public profile by their handle slug."""
    profile = await client.get_profile_by_slug(slug)
    return ProfileResponse.from_substack(profile)


@router.get("/profiles/{slug}/posts", response_model=PostsPageResponse)
async def get_profile_posts(
    slug: str,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    page: Annotated[OffsetPage, Depends()],
) -> PostsPageResponse:
    """Return a page of posts for the given profile slug."""
    result = await client.get_posts_for_slug(slug, limit=page.limit, offset=page.offset)
    return PostsPageResponse.from_substack(result)


@router.get("/profiles/{slug}/notes", response_model=NotesPageResponse)
async def get_profile_notes(
    slug: str,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    page: Annotated[CursorPage, Depends()],
) -> NotesPageResponse:
    """Return a page of notes for the given profile slug."""
    result = await client.get_notes_for_slug(slug, cursor=page.cursor)
    return NotesPageResponse.from_substack(result)
