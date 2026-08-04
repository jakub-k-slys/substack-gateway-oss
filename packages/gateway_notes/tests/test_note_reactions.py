from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from gateway_notes.service import NotesService


@pytest.mark.anyio
async def test_like_note_posts_heart_reaction() -> None:
    sub = AsyncMock()
    service = NotesService(AsyncMock(), sub)

    await service.like_note(234058408)

    sub.post.assert_awaited_once_with(
        "comment/234058408/reaction",
        json={"publication_id": None, "reaction": "❤"},
    )


@pytest.mark.anyio
async def test_unlike_note_deletes_heart_reaction_with_tab_id() -> None:
    sub = AsyncMock()
    service = NotesService(AsyncMock(), sub)

    await service.unlike_note(238483442)

    sub.delete.assert_awaited_once_with(
        "comment/238483442/reaction",
        json={"publication_id": None, "reaction": "❤", "tabId": "for-you"},
    )
