from __future__ import annotations

from unittest.mock import AsyncMock

import httpx
import pytest

from gateway_core.models.substack import SubstackPostComment
from gateway_notes.service import NotesService


def _resp(json: object) -> httpx.Response:
    return httpx.Response(200, json=json, request=httpx.Request("GET", "http://test"))


@pytest.mark.anyio
async def test_reply_to_note_posts_to_comment_feed_with_parent_id() -> None:
    sub = AsyncMock()
    sub.post.return_value = _resp({"id": 999, "date": "2026-08-04", "status": "ok"})
    service = NotesService(AsyncMock(), sub)

    created = await service.reply_to_note(parent_id=234058408, body="hello")

    assert created.id == 999
    sub.post.assert_awaited_once()
    call = sub.post.await_args
    assert call.args[0] == "comment/feed/"
    assert call.kwargs["json"]["parent_id"] == 234058408


@pytest.mark.anyio
async def test_list_note_replies_flattens_comment_branches() -> None:
    sub = AsyncMock()
    sub.get.return_value = _resp(
        {
            "commentBranches": [
                {"comment": {"id": 1, "body": "first"}},
                {"comment": {"id": 2, "body": "second"}},
            ]
        }
    )
    service = NotesService(AsyncMock(), sub)

    replies = await service.list_note_replies(131648795)

    sub.get.assert_awaited_once_with("reader/comment/131648795/replies")
    assert [r.id for r in replies] == [1, 2]
    assert [r.body for r in replies] == ["first", "second"]


def test_post_comment_parent_id_parses_ancestor_path() -> None:
    assert SubstackPostComment(id=1, body="x", ancestor_path="1.2.3").parent_id == 3
    assert SubstackPostComment(id=1, body="x").parent_id is None
    assert SubstackPostComment(id=1, body="x", ancestor_path="").parent_id is None
    assert SubstackPostComment(id=1, body="x", ancestor_path="1.2.x").parent_id is None
