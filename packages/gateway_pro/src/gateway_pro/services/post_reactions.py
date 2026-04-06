from __future__ import annotations

import logging

from gateway_oss.client.substack import SubstackClient

_log = logging.getLogger(__name__)

_LIKE_REACTION = "\u2764"
_READER_SURFACE = "reader"


class PostReactionsService:
    def __init__(self, sub: SubstackClient) -> None:
        self._sub = sub

    async def like_post(self, post_id: int) -> None:
        _log.debug("Adding like to post id=%d", post_id)
        await self._sub.post(
            f"post/{post_id}/reaction",
            json={"reaction": _LIKE_REACTION, "surface": _READER_SURFACE},
        )
        _log.debug("Added like to post id=%d", post_id)

    async def unlike_post(self, post_id: int) -> None:
        _log.debug("Removing like from post id=%d", post_id)
        await self._sub.delete(f"post/{post_id}/reaction", json={})
        _log.debug("Removed like from post id=%d", post_id)
