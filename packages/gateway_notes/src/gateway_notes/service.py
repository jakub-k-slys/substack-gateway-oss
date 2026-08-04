from __future__ import annotations

import logging

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_core.converters.markdown import markdown_to_note_payload
from gateway_core.models.substack import (
    SubstackAttachmentCreated,
    SubstackCommentBranchesResponse,
    SubstackItemResponse,
    SubstackNote,
    SubstackNoteCreated,
    SubstackNotesPage,
    SubstackPostComment,
)

_log = logging.getLogger(__name__)

_LIKE_REACTION = "❤"
_FOR_YOU_TAB_ID = "for-you"


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

    async def get_notes_for_profile(
        self, profile_id: int, cursor: str | None = None
    ) -> SubstackNotesPage:
        """GET /reader/feed/profile/{id}?types=note — notes for a given profile ID."""
        params: dict[str, str] = {"types": "note"}
        if cursor:
            params["cursor"] = cursor
        r = await self._pub.get(f"reader/feed/profile/{profile_id}", params=params)
        return SubstackNotesPage.model_validate(r.json())

    async def _get_reader_comment(self, comment_id: int) -> SubstackNote:
        r = await self._pub.get(f"reader/comment/{comment_id}")
        return SubstackItemResponse.model_validate(r.json()).item

    async def like_note(self, note_id: int) -> None:
        """POST /comment/{id}/reaction — add a heart reaction to a note."""
        _log.debug("Adding like to note id=%d", note_id)
        await self._sub.post(
            f"comment/{note_id}/reaction",
            json={"publication_id": None, "reaction": _LIKE_REACTION},
        )

    async def unlike_note(self, note_id: int) -> None:
        """DELETE /comment/{id}/reaction — remove the heart reaction from a note."""
        _log.debug("Removing like from note id=%d", note_id)
        await self._sub.delete(
            f"comment/{note_id}/reaction",
            json={
                "publication_id": None,
                "reaction": _LIKE_REACTION,
                "tabId": _FOR_YOU_TAB_ID,
            },
        )

    async def reply_to_note(self, parent_id: int, body: str) -> SubstackNoteCreated:
        """POST /comment/feed/ with parent_id — reply to a note or note-comment."""
        _log.debug("Replying to note parent_id=%d", parent_id)
        payload = markdown_to_note_payload(body)
        payload["parent_id"] = parent_id
        r = await self._sub.post("comment/feed/", json=payload)
        created = SubstackNoteCreated.model_validate(r.json())
        _log.debug("Created reply id=%d to parent_id=%d", created.id, parent_id)
        return created

    async def list_note_replies(self, parent_id: int) -> list[SubstackPostComment]:
        """GET /reader/comment/{id}/replies — direct replies in a note thread."""
        _log.debug("Listing replies to parent_id=%d", parent_id)
        r = await self._sub.get(f"reader/comment/{parent_id}/replies")
        page = SubstackCommentBranchesResponse.model_validate(r.json())
        return [b.comment for b in page.branches]
