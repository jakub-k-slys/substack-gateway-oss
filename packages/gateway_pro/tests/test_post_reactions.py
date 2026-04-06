from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from gateway_pro.services.post_reactions import PostReactionsService


@pytest.mark.anyio
async def test_like_post_posts_heart_reaction_with_reader_surface() -> None:
    sub = AsyncMock()
    service = PostReactionsService(sub)

    await service.like_post(191598243)

    sub.post.assert_awaited_once_with(
        "post/191598243/reaction",
        json={"reaction": "\u2764", "surface": "reader"},
    )


@pytest.mark.anyio
async def test_unlike_post_deletes_reaction_with_empty_payload() -> None:
    sub = AsyncMock()
    service = PostReactionsService(sub)

    await service.unlike_post(191598243)

    sub.delete.assert_awaited_once_with("post/191598243/reaction", json={})
