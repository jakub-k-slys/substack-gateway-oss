from __future__ import annotations

import logging

from gateway_oss.client.substack import SubstackClient

_log = logging.getLogger(__name__)


class PostRestacksService:
    def __init__(self, sub: SubstackClient) -> None:
        self._sub = sub

    async def restack_post(self, post_id: int) -> None:
        _log.debug("Restacking post id=%d", post_id)
        await self._sub.post(
            "restack/feed",
            json={"postId": post_id, "commentId": None},
        )
        _log.debug("Restacked post id=%d", post_id)
