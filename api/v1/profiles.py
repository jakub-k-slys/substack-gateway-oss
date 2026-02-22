from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_substack_client
from client.exceptions import SubstackAPIError, SubstackAuthError
from client.substack import SubstackClient
from models.schemas import (
    NoteResponse,
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)

router = APIRouter()


@router.get("/profiles/{slug}", response_model=ProfileResponse)
async def get_profile(
    slug: str,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> ProfileResponse:
    try:
        profile = await client.get_profile_by_slug(slug)
    except SubstackAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SubstackAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return ProfileResponse.from_substack(profile)


@router.get("/profiles/{slug}/posts", response_model=PostsPageResponse)
async def get_profile_posts(
    slug: str,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    limit: int = 25,
    offset: int = 0,
) -> PostsPageResponse:
    try:
        profile = await client.get_profile_by_slug(slug)
        page = await client.get_posts_for_profile(
            profile.id, limit=limit, offset=offset
        )
    except SubstackAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SubstackAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return PostsPageResponse.from_substack(page)


@router.get("/profiles/{slug}/notes", response_model=NotesPageResponse)
async def get_profile_notes(
    slug: str,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    cursor: str | None = None,
) -> NotesPageResponse:
    try:
        profile = await client.get_profile_by_slug(slug)
        page = await client.get_notes_for_profile(profile.id, cursor=cursor)
    except SubstackAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SubstackAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return NotesPageResponse(
        items=[NoteResponse.from_substack(n) for n in page.items],
        next_cursor=page.nextCursor,
    )
