from __future__ import annotations

from gateway_core.models.substack import (
    SubstackNote,
    SubstackNoteComment,
    SubstackNoteContext,
)
from gateway_notes.schemas import NoteResponse


def test_note_response_omits_author_when_note_has_no_users() -> None:
    note = SubstackNote(
        entity_key="comment-247947616",
        context=SubstackNoteContext(
            timestamp="2026-04-23T13:46:04.396Z",
            users=[],
        ),
        comment=SubstackNoteComment(
            id=247947616,
            body="Reflection isn't always enlightening.",
            reaction_count=3,
        ),
    )

    response = NoteResponse.from_substack(note).model_dump(exclude_none=True)

    assert response == {
        "id": 247947616,
        "body": "Reflection isn't always enlightening.",
        "likes_count": 3,
        "published_at": "2026-04-23T13:46:04.396Z",
    }
