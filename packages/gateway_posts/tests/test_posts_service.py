from __future__ import annotations

from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock

import pytest

from gateway_posts.service import PostsService


def _service(sub: AsyncMock) -> PostsService:
    response = MagicMock()
    response.json.return_value = {"posts": [], "nextCursor": None}
    sub.get.return_value = response
    return PostsService(cast(Any, None), sub)


@pytest.mark.anyio
async def test_profile_posts_first_page_sends_no_cursor() -> None:
    sub = AsyncMock()
    await _service(sub).get_posts_for_profile(42, limit=50)

    sub.get.assert_awaited_once_with(
        "profile/posts", params={"profile_user_id": 42, "limit": 50}
    )


@pytest.mark.anyio
async def test_profile_posts_sends_cursor_as_next_cursor() -> None:
    # Substack's profile/posts reads `next_cursor`; a `cursor` param is ignored
    # and the first page comes back again.
    sub = AsyncMock()
    await _service(sub).get_posts_for_profile(42, limit=50, cursor="abc")

    sub.get.assert_awaited_once_with(
        "profile/posts",
        params={"profile_user_id": 42, "limit": 50, "next_cursor": "abc"},
    )
