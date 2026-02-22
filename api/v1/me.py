from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from api.deps import get_substack_client
from client.substack import SubstackClient
from models.schemas import (
    FollowingResponse,
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)

router = APIRouter()


@router.get("/me", response_model=ProfileResponse)
async def get_me(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> ProfileResponse:
    """Return the authenticated user's own Substack profile."""
    profile = await client.get_own_profile()
    return ProfileResponse.from_substack(profile)


@router.get("/me/notes", response_model=NotesPageResponse)
async def get_me_notes(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    cursor: str | None = None,
) -> NotesPageResponse:
    """Return a page of the authenticated user's own notes."""
    page = await client.get_own_notes(cursor=cursor)
    return NotesPageResponse.from_substack(page)


@router.get("/me/posts", response_model=PostsPageResponse)
async def get_me_posts(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    limit: int = Query(default=25, gt=0, le=100),
    offset: int = Query(default=0, ge=0),
) -> PostsPageResponse:
    """Return a page of the authenticated user's own posts."""
    page = await client.get_own_posts(limit=limit, offset=offset)
    return PostsPageResponse.from_substack(page)


@router.get("/me/following", response_model=FollowingResponse)
async def get_me_following(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> FollowingResponse:
    """Return the list of users the authenticated user follows."""
    users = await client.get_own_following()
    return FollowingResponse.from_substack(users)
