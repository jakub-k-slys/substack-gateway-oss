from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_substack_client
from client.exceptions import SubstackAPIError, SubstackAuthError
from client.substack import SubstackClient
from models.schemas import (
    NoteResponse,
    NotesPageResponse,
    PostResponse,
    PostsPageResponse,
    ProfileResponse,
)

router = APIRouter()


@router.get("/me", response_model=ProfileResponse)
async def get_me(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> ProfileResponse:
    try:
        profile = await client.get_own_profile()
    except SubstackAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SubstackAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return ProfileResponse.from_substack(profile)


@router.get("/me/notes", response_model=NotesPageResponse)
async def get_me_notes(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    cursor: str | None = None,
) -> NotesPageResponse:
    try:
        page = await client.get_own_notes(cursor=cursor)
    except SubstackAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SubstackAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return NotesPageResponse(
        items=[NoteResponse.from_substack(n) for n in page.items],
        next_cursor=page.nextCursor,
    )


@router.get("/me/posts", response_model=PostsPageResponse)
async def get_me_posts(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    limit: int = 25,
    offset: int = 0,
) -> PostsPageResponse:
    try:
        posts = await client.get_own_posts(limit=limit, offset=offset)
    except SubstackAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SubstackAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return PostsPageResponse(items=[PostResponse.from_substack(p) for p in posts])
