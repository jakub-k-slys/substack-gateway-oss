from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from typing import Any

from gateway_core.auth import (
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_notes.schemas import CreateNoteResponse, NoteResponse
from gateway_notes.service import NotesService


@contextlib.asynccontextmanager
async def _authenticated_clients(
    token: str,
) -> AsyncIterator[tuple[PublicationClient, SubstackClient]]:
    credentials = decode_bearer_credentials(token)
    assert credentials.publication_url is not None
    async with (
        make_publication_client(credentials, credentials.publication_url) as pub,
        make_substack_client(credentials) as sub,
    ):
        yield pub, sub


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
