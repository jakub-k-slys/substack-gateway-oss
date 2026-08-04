from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from gateway_comments.service import CommentNotFoundError, CommentsService


def _resp(payload):
    r = AsyncMock()
    r.json = lambda: payload
    return r


@pytest.mark.anyio
async def test_create_top_level_comment_posts_body():
    pub = AsyncMock()
    pub.post.return_value = _resp({"id": 5, "body": "hi"})
    out = await CommentsService(pub, AsyncMock()).create_top_level_comment(99, "hi")
    pub.post.assert_awaited_once_with("post/99/comment", json={"body": "hi"})
    assert out.id == 5 and out.body == "hi"


@pytest.mark.anyio
async def test_reply_to_comment_resolves_post_then_posts_with_parent_id():
    pub = AsyncMock()
    # first GET reader/comment/{id} resolves the post id, then POST creates the reply
    pub.get.return_value = _resp(
        {
            "item": {
                "entity_key": "k",
                "context": {
                    "type": "feed",
                    "timestamp": "2026-01-01T00:00:00Z",
                    "users": [],
                },
                "post": {"id": 77, "title": "t", "post_date": "2026-01-01T00:00:00Z"},
            }
        }
    )
    pub.post.return_value = _resp({"id": 6, "body": "re"})
    out = await CommentsService(pub, AsyncMock()).reply_to_comment(42, "re")
    pub.get.assert_awaited_once_with("reader/comment/42")
    pub.post.assert_awaited_once_with(
        "post/77/comment", json={"body": "re", "parent_id": 42}
    )
    assert out.id == 6


@pytest.mark.anyio
async def test_reply_to_comment_raises_when_no_post():
    pub = AsyncMock()
    pub.get.return_value = _resp(
        {
            "item": {
                "entity_key": "k",
                "context": {
                    "type": "feed",
                    "timestamp": "2026-01-01T00:00:00Z",
                    "users": [],
                },
                "post": None,
            }
        }
    )
    with pytest.raises(CommentNotFoundError):
        await CommentsService(pub, AsyncMock()).reply_to_comment(42, "re")


@pytest.mark.anyio
async def test_get_post_comment_maps_reader_note_to_post_comment():
    pub = AsyncMock()
    pub.get.return_value = _resp(
        {
            "item": {
                "entity_key": "k",
                "context": {
                    "type": "feed",
                    "timestamp": "2026-01-01T00:00:00Z",
                    "users": [],
                },
                "post": {"id": 77, "title": "t", "post_date": "2026-01-01T00:00:00Z"},
                "comment": {
                    "id": 9,
                    "body": "b",
                    "name": "Ann",
                    "photo_url": "u",
                    "reaction_count": 3,
                },
            }
        }
    )
    out = await CommentsService(pub, AsyncMock()).get_post_comment(9)
    pub.get.assert_awaited_once_with("reader/comment/9")
    assert out.id == 9 and out.post_id == 77 and out.name == "Ann"
    assert out.reaction_count == 3


@pytest.mark.anyio
async def test_delete_comment_calls_delete():
    pub = AsyncMock()
    await CommentsService(pub, AsyncMock()).delete_comment(9)
    pub.delete.assert_awaited_once_with("comment/9")


@pytest.mark.anyio
async def test_list_comment_replies_unwraps_branches():
    pub = AsyncMock()
    pub.get.return_value = _resp(
        {
            "commentBranches": [
                {"comment": {"id": 1, "body": "a"}},
                {"comment": {"id": 2, "body": "b"}},
            ]
        }
    )
    out = await CommentsService(pub, AsyncMock()).list_comment_replies(42)
    pub.get.assert_awaited_once_with("reader/comment/42/replies")
    assert [c.id for c in out] == [1, 2]
