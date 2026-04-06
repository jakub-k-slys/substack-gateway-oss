from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from gateway_oss.api.deps import get_credentials

from gateway_pro.api.deps import get_note_reactions_service
from gateway_pro.services.note_reactions import NoteReactionsService

router = APIRouter(tags=["notes"])


@router.put(
    "/notes/{note_id}/like",
    status_code=204,
    dependencies=[Depends(get_credentials)],
)
async def like_note(
    note_id: Annotated[int, Path(gt=0)],
    service: Annotated[NoteReactionsService, Depends(get_note_reactions_service)],
) -> None:
    """Add a like to a Substack note."""
    await service.like_note(note_id)


@router.delete(
    "/notes/{note_id}/like",
    status_code=204,
    dependencies=[Depends(get_credentials)],
)
async def unlike_note(
    note_id: Annotated[int, Path(gt=0)],
    service: Annotated[NoteReactionsService, Depends(get_note_reactions_service)],
) -> None:
    """Remove a like from a Substack note."""
    await service.unlike_note(note_id)
