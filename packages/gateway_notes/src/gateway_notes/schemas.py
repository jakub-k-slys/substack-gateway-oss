from __future__ import annotations

import logging

from pydantic import BaseModel

from gateway_core.models.substack import (
    SubstackNote,
    SubstackNoteCreated,
    SubstackNotesPage,
)

_log = logging.getLogger(__name__)


class NoteAuthor(BaseModel):
    id: int
    name: str
    handle: str
    avatar_url: str


class NoteResponse(BaseModel):
    id: int
    body: str
    likes_count: int
    author: NoteAuthor | None = None
    published_at: str

    @classmethod
    def from_substack(cls, note: SubstackNote) -> NoteResponse:
        user = note.context.users[0] if note.context.users else None
        comment = note.comment
        if comment is None:
            _log.warning(
                "Note %r has no comment body; returning empty defaults", note.entity_key
            )
        if user is None:
            _log.warning(
                "Note %r has no author; returning empty defaults", note.entity_key
            )
        return cls(
            id=comment.id if comment else 0,
            body=comment.body if comment else "",
            likes_count=comment.reaction_count
            if (comment and comment.reaction_count is not None)
            else 0,
            author=(
                NoteAuthor(
                    id=user.id,
                    name=user.name,
                    handle=user.handle,
                    avatar_url=user.photo_url or "",
                )
                if user
                else None
            ),
            published_at=note.context.timestamp,
        )


class NotesPageResponse(BaseModel):
    items: list[NoteResponse]
    next: str | None = None

    @classmethod
    def from_substack(cls, page: SubstackNotesPage) -> NotesPageResponse:
        return cls(
            items=[NoteResponse.from_substack(n) for n in page.items],
            next=page.next_cursor,
        )


class CreateNoteRequest(BaseModel):
    content: str
    attachment: str | None = None


class CreateNoteResponse(BaseModel):
    id: int

    @classmethod
    def from_substack(cls, note: SubstackNoteCreated) -> CreateNoteResponse:
        return cls(id=note.id)
