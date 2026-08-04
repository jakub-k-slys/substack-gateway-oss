from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from gateway_comments.service import CommentsService


@pytest.mark.anyio
async def test_like_comment_posts_heart_via_publication_client():
    pub = AsyncMock()
    await CommentsService(pub, AsyncMock()).like_comment(9)
    pub.post.assert_awaited_once_with(
        "comment/9/reaction", json={"publication_id": None, "reaction": "❤"}
    )


@pytest.mark.anyio
async def test_unlike_comment_deletes_heart_without_tab_id():
    pub = AsyncMock()
    await CommentsService(pub, AsyncMock()).unlike_comment(9)
    pub.delete.assert_awaited_once_with(
        "comment/9/reaction", json={"publication_id": None, "reaction": "❤"}
    )
