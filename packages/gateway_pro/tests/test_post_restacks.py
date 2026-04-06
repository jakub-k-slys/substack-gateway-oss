from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from gateway_pro.services.post_restacks import PostRestacksService


@pytest.mark.anyio
async def test_restack_post_posts_feed_restack_payload() -> None:
    sub = AsyncMock()
    service = PostRestacksService(sub)

    await service.restack_post(191598243)

    sub.post.assert_awaited_once_with(
        "restack/feed",
        json={"postId": 191598243, "commentId": None},
    )
