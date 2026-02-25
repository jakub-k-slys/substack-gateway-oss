from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from api.deps import get_substack_client
from client.substack import SubstackClient
from models.pagination import CursorPage, OffsetPage
from models.schemas import (
    FollowingResponse,
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)

router = APIRouter(tags=["me"])


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
    page: Annotated[CursorPage, Depends()],
) -> NotesPageResponse:
    """Return a page of the authenticated user's own notes."""
    result = await client.get_own_notes(cursor=page.cursor)
    return NotesPageResponse.from_substack(result)


@router.get("/me/posts", response_model=PostsPageResponse)
async def get_me_posts(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    page: Annotated[OffsetPage, Depends()],
) -> PostsPageResponse:
    """Return a page of the authenticated user's own posts."""
    result = await client.get_own_posts(limit=page.limit, offset=page.offset)
    return PostsPageResponse.from_substack(result)


@router.get("/me/following", response_model=FollowingResponse)
async def get_me_following(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> FollowingResponse:
    """Return the list of users the authenticated user follows."""
    users = await client.get_own_following()
    return FollowingResponse.from_substack(users)
