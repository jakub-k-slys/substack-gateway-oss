from __future__ import annotations

import logging

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_core.models.substack import (
    SubstackComment,
    SubstackCommentBranchesResponse,
    SubstackCommentsResponse,
    SubstackItemResponse,
    SubstackNote,
    SubstackPostComment,
)

_log = logging.getLogger(__name__)

_LIKE_REACTION = "❤"


class CommentNotFoundError(Exception):
    """Raised when a parent comment cannot be resolved to a post."""


class CommentsService:
    def __init__(self, pub: PublicationClient, sub: SubstackClient) -> None:
        self._pub = pub
        self._sub = sub

    async def get_comments_for_post(self, post_id: int) -> list[SubstackComment]:
        """GET /post/{id}/comments — all comments for a post."""
        r = await self._pub.get(f"post/{post_id}/comments")
        return SubstackCommentsResponse.model_validate(r.json()).comments

    async def get_comment_by_id(self, comment_id: int) -> SubstackNote:
        """GET /reader/comment/{id} — a single comment in the reader wire format."""
        return await self._get_reader_comment(comment_id)

    async def create_top_level_comment(
        self, post_id: int, body: str
    ) -> SubstackPostComment:
        """POST /post/{post_id}/comment — top-level comment under a post."""
        r = await self._pub.post(f"post/{post_id}/comment", json={"body": body})
        return SubstackPostComment.model_validate(r.json())

    async def reply_to_comment(
        self, parent_comment_id: int, body: str
    ) -> SubstackPostComment:
        """POST /post/{post_id}/comment with parent_id — reply to a comment."""
        parent_post_id = await self._resolve_post_id(parent_comment_id)
        r = await self._pub.post(
            f"post/{parent_post_id}/comment",
            json={"body": body, "parent_id": parent_comment_id},
        )
        return SubstackPostComment.model_validate(r.json())

    async def get_post_comment(self, comment_id: int) -> SubstackPostComment:
        """GET /reader/comment/{id} — a single comment in the rich comment shape."""
        note = await self._get_reader_comment(comment_id)
        return self._note_to_post_comment(note)

    async def delete_comment(self, comment_id: int) -> None:
        """DELETE /comment/{id} — delete a comment under a post."""
        await self._pub.delete(f"comment/{comment_id}")

    async def list_comment_replies(self, comment_id: int) -> list[SubstackPostComment]:
        """GET /reader/comment/{id}/replies — direct replies to a comment."""
        r = await self._pub.get(f"reader/comment/{comment_id}/replies")
        page = SubstackCommentBranchesResponse.model_validate(r.json())
        return [b.comment for b in page.branches]

    async def like_comment(self, comment_id: int) -> None:
        """POST /comment/{id}/reaction — add a heart reaction to a comment."""
        await self._pub.post(
            f"comment/{comment_id}/reaction",
            json={"publication_id": None, "reaction": _LIKE_REACTION},
        )

    async def unlike_comment(self, comment_id: int) -> None:
        """DELETE /comment/{id}/reaction — remove the heart reaction."""
        await self._pub.delete(
            f"comment/{comment_id}/reaction",
            json={"publication_id": None, "reaction": _LIKE_REACTION},
        )

    async def _resolve_post_id(self, comment_id: int) -> int:
        note = await self._get_reader_comment(comment_id)
        if note.post is None or note.post.id is None:
            raise CommentNotFoundError(f"comment {comment_id} has no associated post")
        return note.post.id

    async def _get_reader_comment(self, comment_id: int) -> SubstackNote:
        r = await self._pub.get(f"reader/comment/{comment_id}")
        return SubstackItemResponse.model_validate(r.json()).item

    @staticmethod
    def _note_to_post_comment(note: SubstackNote) -> SubstackPostComment:
        c = note.comment
        post_id = note.post.id if note.post else None
        if c is None:
            raise CommentNotFoundError("reader/comment response missing 'comment'")
        return SubstackPostComment(
            id=c.id,
            body=c.body,
            post_id=post_id,
            name=c.name,
            photo_url=c.photo_url,
            reaction_count=c.reaction_count,
        )
