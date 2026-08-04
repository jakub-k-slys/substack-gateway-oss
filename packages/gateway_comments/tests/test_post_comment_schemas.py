from __future__ import annotations

from gateway_comments.schemas import PostCommentRepliesResponse, PostCommentResponse
from gateway_core.models.substack import SubstackPostComment


def test_post_comment_response_from_substack_maps_fields():
    c = SubstackPostComment(
        id=1,
        body="b",
        post_id=7,
        user_id=3,
        date="2026-01-01",
        deleted=False,
        name="Ann",
        ancestor_path="1.2",
        reaction_count=4,
    )
    out = PostCommentResponse.from_substack(c)
    assert out.id == 1 and out.post_id == 7 and out.parent_id == 2
    assert out.author_name == "Ann" and out.reaction_count == 4


def test_post_comment_replies_response_wraps_items():
    c = SubstackPostComment(id=2, body="r")
    out = PostCommentRepliesResponse.from_substack([c])
    assert len(out.items) == 1 and out.items[0].id == 2
