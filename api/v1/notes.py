from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from api.deps import get_substack_client
from client.substack import SubstackClient
from models.schemas import NoteResponse

router = APIRouter()


@router.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> NoteResponse:
    """Return a single Substack note by its ID."""
    note = await client.get_note_by_id(note_id)
    return NoteResponse.from_substack(note)
