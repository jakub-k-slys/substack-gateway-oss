from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path

from gateway.api.deps import get_notes_service
from gateway.models.schemas import NoteResponse
from gateway.services.notes import NotesService

router = APIRouter(tags=["comments"])


@router.get("/comments/{comment_id}", response_model=NoteResponse)
async def get_comment(
    comment_id: Annotated[int, Path(gt=0)],
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> NoteResponse:
    """Return a single Substack comment by its ID (uses the reader comment wire format)."""
    comment = await service.get_comment_by_id(comment_id)
    return NoteResponse.from_substack(comment)
