from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_substack_client
from client.exceptions import SubstackAPIError, SubstackAuthError
from client.substack import SubstackClient
from models.schemas import CommentResponse, CommentsResponse, FullPostResponse

router = APIRouter()


@router.get("/posts/{post_id}", response_model=FullPostResponse)
async def get_post(
    post_id: int,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> FullPostResponse:
    try:
        post = await client.get_post_by_id(post_id)
    except SubstackAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SubstackAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return FullPostResponse.from_substack(post)


@router.get("/posts/{post_id}/comments", response_model=CommentsResponse)
async def get_post_comments(
    post_id: int,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> CommentsResponse:
    try:
        comments = await client.get_comments_for_post(post_id)
    except SubstackAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SubstackAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return CommentsResponse(items=[CommentResponse.from_substack(c) for c in comments])
