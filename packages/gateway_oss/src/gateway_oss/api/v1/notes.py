from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from gateway_oss.api.deps import get_notes_service
from gateway_oss.models.schemas import (
    CreateNoteRequest,
    CreateNoteResponse,
    NoteResponse,
)
from gateway_oss.services.notes import NotesService

router = APIRouter(tags=["notes"])


@router.get(
    "/notes/{note_id}",
    response_model=NoteResponse,
    response_model_exclude_none=True,
)
async def get_note(
    note_id: Annotated[int, Path(gt=0)],
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> NoteResponse:
    """Return a single Substack note by its ID."""
    note = await service.get_note_by_id(note_id)
    return NoteResponse.from_substack(note)


@router.delete("/notes/{note_id}", status_code=204)
async def delete_note(
    note_id: Annotated[int, Path(gt=0)],
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> None:
    """Delete a Substack note by its ID."""
    await service.delete_note(note_id)


@router.post("/notes", response_model=CreateNoteResponse, status_code=201)
async def create_note(
    body: CreateNoteRequest,
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> CreateNoteResponse:
    """Convert markdown content to a Substack note and publish it."""
    try:
        note = await service.create_note(body.content, attachment=body.attachment)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CreateNoteResponse.from_substack(note)
