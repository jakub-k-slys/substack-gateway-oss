from __future__ import annotations

from gateway_core.models.substack import SubstackComment, SubstackCommentsResponse
from gateway_posts.service import PostsService as _PostsService


class PostsService(_PostsService):
    """OSS-local extension of gateway_posts' PostsService.

    get_comments_for_post has not been extracted into gateway_comments yet
    (that lands in a later fleet-split task); it is kept here so the OSS
    post-comments API route and MCP tool keep working in the meantime. This
    mirrors the plan-mandated get_notes_for_profile duplication elsewhere in
    the fleet split.
    """

    async def get_comments_for_post(self, post_id: int) -> list[SubstackComment]:
        """GET /post/{id}/comments — all comments for a post."""
        r = await self._pub.get(f"post/{post_id}/comments")
        return SubstackCommentsResponse.model_validate(r.json()).comments
