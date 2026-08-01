from __future__ import annotations

from typing import Any

from gateway_comments.schemas import CommentsResponse
from gateway_comments.service import CommentsService
from gateway_mcp_common.clients import _authenticated_clients


async def get_post_comments(post_id: int, token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        comments = await CommentsService(pub, sub).get_comments_for_post(post_id)
    return CommentsResponse.from_substack(comments).model_dump()
