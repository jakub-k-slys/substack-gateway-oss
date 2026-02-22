from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_substack_client
from client.exceptions import SubstackAPIError, SubstackAuthError
from client.substack import SubstackClient
from models.schemas import NoteResponse

router = APIRouter()


@router.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> NoteResponse:
    try:
        note = await client.get_note_by_id(note_id)
    except SubstackAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SubstackAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return NoteResponse.from_substack(note)
