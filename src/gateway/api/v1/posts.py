from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path

from gateway.api.deps import get_substack_client
from gateway.client.substack import SubstackClient
from gateway.models.schemas import CommentsResponse, FullPostResponse

router = APIRouter(tags=["posts"])


@router.get("/posts/{post_id}", response_model=FullPostResponse)
async def get_post(
    post_id: Annotated[int, Path(gt=0)],
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> FullPostResponse:
    """Return a single Substack post with its full content."""
    post = await client.get_post_by_id(post_id)
    return FullPostResponse.from_substack(post)


@router.get("/posts/{post_id}/comments", response_model=CommentsResponse)
async def get_post_comments(
    post_id: Annotated[int, Path(gt=0)],
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> CommentsResponse:
    """Return comments for the given post."""
    comments = await client.get_comments_for_post(post_id)
    return CommentsResponse.from_substack(comments)
