from __future__ import annotations

from typing import Any

from gateway_following.schemas import FollowingResponse
from gateway_following.service import FollowingService
from gateway_mcp_common.clients import _authenticated_clients


async def get_my_following(token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (pub, sub):
        users = await FollowingService(pub, sub).get_own_following()
    return FollowingResponse.from_substack(users).model_dump()
