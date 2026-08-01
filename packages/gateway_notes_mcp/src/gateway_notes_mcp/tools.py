from __future__ import annotations

from typing import Any

from gateway_mcp_common.clients import _authenticated_clients
from gateway_notes.schemas import CreateNoteResponse, NoteResponse
from gateway_notes.service import NotesService


async def get_note(note_id: int, token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        note = await NotesService(pub, sub).get_note_by_id(note_id)
    return NoteResponse.from_substack(note).model_dump(exclude_none=True)


async def create_note(
    content: str, token: str, attachment: str | None = None
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        note = await NotesService(pub, sub).create_note(content, attachment=attachment)
    return CreateNoteResponse.from_substack(note).model_dump()


async def delete_note(note_id: int, token: str) -> str:
    async with _authenticated_clients(token) as (pub, sub):
        await NotesService(pub, sub).delete_note(note_id)
    return f"Note {note_id} deleted successfully."
