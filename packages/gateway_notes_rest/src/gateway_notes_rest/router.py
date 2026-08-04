from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field

from gateway_notes.schemas import (
    CreateNoteRequest,
    CreateNoteResponse,
    NoteRepliesResponse,
    NoteReplyCreatedResponse,
    NoteResponse,
)
from gateway_notes.service import NotesService
from gateway_notes_rest.deps import get_notes_service
from gateway_rest_common.deps import get_credentials

router = APIRouter(tags=["notes"])


class NoteReplyRequest(BaseModel):
    body: str = Field(min_length=1)


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


@router.put(
    "/notes/{note_id}/like",
    status_code=204,
    dependencies=[Depends(get_credentials)],
)
async def like_note(
    note_id: Annotated[int, Path(gt=0)],
    service: Annotated[NotesService, Depends(get_notes_service)],
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
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> None:
    """Remove a like from a Substack note."""
    await service.unlike_note(note_id)


@router.post(
    "/notes/{note_id}/comments",
    response_model=NoteReplyCreatedResponse,
    response_model_exclude_none=True,
    status_code=201,
    dependencies=[Depends(get_credentials)],
)
async def reply_to_note(
    note_id: Annotated[int, Path(gt=0)],
    payload: NoteReplyRequest,
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> NoteReplyCreatedResponse:
    """Reply to a note or to any comment in a note thread."""
    created = await service.reply_to_note(parent_id=note_id, body=payload.body)
    return NoteReplyCreatedResponse.from_substack(created)


@router.get(
    "/notes/{note_id}/comments",
    response_model=NoteRepliesResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(get_credentials)],
)
async def list_note_replies(
    note_id: Annotated[int, Path(gt=0)],
    service: Annotated[NotesService, Depends(get_notes_service)],
) -> NoteRepliesResponse:
    """List direct replies to a note (or any node in its thread)."""
    replies = await service.list_note_replies(note_id)
    return NoteRepliesResponse.from_substack(replies)
