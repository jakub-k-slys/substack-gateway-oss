from __future__ import annotations

import logging

from gateway.client.publication import PublicationClient
from gateway.client.substack import SubstackClient
from gateway.converters.markdown import markdown_to_note_payload
from gateway.models.substack import (
    SubstackAttachmentCreated,
    SubstackItemResponse,
    SubstackNote,
    SubstackNoteCreated,
    SubstackNotesPage,
)

_log = logging.getLogger(__name__)


class NotesService:
    def __init__(self, pub: PublicationClient, sub: SubstackClient) -> None:
        self._pub = pub
        self._sub = sub

    async def get_own_notes(self, cursor: str | None = None) -> SubstackNotesPage:
        """GET /notes — own notes with optional cursor."""
        _log.debug("Fetching own notes (cursor=%r)", cursor)
        params = {"cursor": cursor} if cursor else {}
        r = await self._pub.get("notes", params=params)
        page = SubstackNotesPage.model_validate(r.json())
        _log.debug(
            "Got %d own notes (next_cursor=%r)", len(page.items), page.next_cursor
        )
        return page

    async def get_note_by_id(self, note_id: int) -> SubstackNote:
        """GET /reader/comment/{id} — fetch a note by ID."""
        _log.debug("Fetching note id=%d", note_id)
        return await self._get_reader_comment(note_id)

    async def get_comment_by_id(self, comment_id: int) -> SubstackNote:
        """GET /reader/comment/{id} — fetch a comment by ID."""
        _log.debug("Fetching comment id=%d", comment_id)
        return await self._get_reader_comment(comment_id)

    async def delete_note(self, note_id: int) -> None:
        """DELETE /comment/{note_id}."""
        _log.debug("Deleting note id=%d", note_id)
        await self._pub.delete(f"comment/{note_id}")
        _log.debug("Deleted note id=%d", note_id)

    async def create_attachment(self, url: str) -> SubstackAttachmentCreated:
        """POST /comment/attachment/ — register a link attachment, returns its UUID."""
        _log.debug("Creating attachment for url=%r", url)
        r = await self._sub.post(
            "comment/attachment/",
            json={"url": url, "type": "link"},
        )
        attachment = SubstackAttachmentCreated.model_validate(r.json())
        _log.debug("Created attachment id=%r", attachment.id)
        return attachment

    async def create_note(
        self, content: str, attachment: str | None = None
    ) -> SubstackNoteCreated:
        """Convert Markdown to a Substack note payload and POST to /comment/feed/."""
        _log.debug("Creating note (%d chars of markdown)", len(content))
        attachment_ids: list[str] | None = None
        if attachment:
            att = await self.create_attachment(attachment)
            attachment_ids = [att.id]
        payload = markdown_to_note_payload(content, attachment_ids=attachment_ids)
        r = await self._sub.post("comment/feed/", json=payload)
        note = SubstackNoteCreated.model_validate(r.json())
        _log.debug("Created note id=%d", note.id)
        return note

    async def _get_reader_comment(self, comment_id: int) -> SubstackNote:
        r = await self._pub.get(f"reader/comment/{comment_id}")
        return SubstackItemResponse.model_validate(r.json()).item
