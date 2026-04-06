from __future__ import annotations

import logging

from gateway_oss.client.substack import SubstackClient

_log = logging.getLogger(__name__)

_LIKE_REACTION = "\u2764"
_FOR_YOU_TAB_ID = "for-you"


class NoteReactionsService:
    def __init__(self, sub: SubstackClient) -> None:
        self._sub = sub

    async def like_note(self, note_id: int) -> None:
        _log.debug("Adding like to note id=%d", note_id)
        await self._sub.post(
            f"comment/{note_id}/reaction",
            json={"publication_id": None, "reaction": _LIKE_REACTION},
        )
        _log.debug("Added like to note id=%d", note_id)

    async def unlike_note(self, note_id: int) -> None:
        _log.debug("Removing like from note id=%d", note_id)
        await self._sub.delete(
            f"comment/{note_id}/reaction",
            json={
                "publication_id": None,
                "reaction": _LIKE_REACTION,
                "tabId": _FOR_YOU_TAB_ID,
            },
        )
        _log.debug("Removed like from note id=%d", note_id)
