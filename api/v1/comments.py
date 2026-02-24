from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path

from api.deps import get_substack_client
from client.substack import SubstackClient
from models.schemas import NoteResponse

router = APIRouter(tags=["comments"])


@router.get("/comments/{comment_id}", response_model=NoteResponse)
async def get_comment(
    comment_id: Annotated[int, Path(gt=0)],
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> NoteResponse:
    """Return a single Substack comment by its ID (uses the reader comment wire format)."""
    comment = await client.get_comment_by_id(comment_id)
    return NoteResponse.from_substack(comment)
