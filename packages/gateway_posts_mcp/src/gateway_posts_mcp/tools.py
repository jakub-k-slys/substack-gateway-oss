from __future__ import annotations

from typing import Any

from gateway_mcp_common.clients import _authenticated_clients
from gateway_posts.schemas import FullPostResponse
from gateway_posts.service import PostsService


async def get_post(post_id: int, token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        post = await PostsService(pub, sub).get_post_by_id(post_id)
    return FullPostResponse.from_substack(post).model_dump()
