from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from api.deps import get_substack_client
from client.substack import SubstackClient
from models.schemas import (
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
    limit: int = Query(default=25, gt=0, le=100),
    offset: int = Query(default=0, ge=0),
) -> PostsPageResponse:
    """Return a page of posts for the given profile slug."""
    profile_id = await client.get_profile_id_by_slug(slug)
    page = await client.get_posts_for_profile(profile_id, limit=limit, offset=offset)
    return PostsPageResponse.from_substack(page)


@router.get("/profiles/{slug}/notes", response_model=NotesPageResponse)
async def get_profile_notes(
    slug: str,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    cursor: str | None = None,
) -> NotesPageResponse:
    """Return a page of notes for the given profile slug."""
    profile_id = await client.get_profile_id_by_slug(slug)
    page = await client.get_notes_for_profile(profile_id, cursor=cursor)
    return NotesPageResponse.from_substack(page)
