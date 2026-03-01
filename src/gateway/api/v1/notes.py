from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from gateway.api.deps import get_substack_client
from gateway.client.substack import SubstackClient
from gateway.models.schemas import CreateNoteRequest, CreateNoteResponse, NoteResponse

router = APIRouter(tags=["notes"])


@router.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: Annotated[int, Path(gt=0)],
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> NoteResponse:
    """Return a single Substack note by its ID."""
    note = await client.get_note_by_id(note_id)
    return NoteResponse.from_substack(note)


@router.delete("/notes/{note_id}", status_code=204)
async def delete_note(
    note_id: Annotated[int, Path(gt=0)],
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> None:
    """Delete a Substack note by its ID."""
    await client.delete_note(note_id)


@router.post("/notes", response_model=CreateNoteResponse, status_code=201)
async def create_note(
    body: CreateNoteRequest,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> CreateNoteResponse:
    """Convert markdown content to a Substack note and publish it."""
    try:
        note = await client.create_note(body.content, attachment=body.attachment)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CreateNoteResponse.from_substack(note)
