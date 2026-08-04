from __future__ import annotations

from typing import Any

from gateway_mcp_common.clients import _authenticated_clients
from gateway_notes.schemas import (
    CreateNoteResponse,
    NoteRepliesResponse,
    NoteReplyCreatedResponse,
    NoteResponse,
)
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


async def like_note(note_id: int, token: str) -> str:
    async with _authenticated_clients(token) as (pub, sub):
        await NotesService(pub, sub).like_note(note_id)
    return f"Note {note_id} liked successfully."


async def unlike_note(note_id: int, token: str) -> str:
    async with _authenticated_clients(token) as (pub, sub):
        await NotesService(pub, sub).unlike_note(note_id)
    return f"Note {note_id} unliked successfully."


async def reply_to_note(note_id: int, body: str, token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        created = await NotesService(pub, sub).reply_to_note(note_id, body)
    return NoteReplyCreatedResponse.from_substack(created).model_dump(exclude_none=True)


async def list_note_replies(note_id: int, token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        replies = await NotesService(pub, sub).list_note_replies(note_id)
    return NoteRepliesResponse.from_substack(replies).model_dump(exclude_none=True)
