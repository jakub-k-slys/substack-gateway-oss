from __future__ import annotations

from typing import Any

from gateway_mcp_common.clients import _authenticated_clients
from gateway_notes.schemas import NotesPageResponse
from gateway_notes.service import NotesService
from gateway_posts.schemas import PostsPageResponse
from gateway_posts.service import PostsService
from gateway_profiles.schemas import ProfileResponse
from gateway_profiles.service import ProfilesService


async def get_me(token: str) -> dict[str, Any]:
    async with _authenticated_clients(token) as (_publication, substack):
        profile = await ProfilesService(substack).get_own_profile()
    return ProfileResponse.from_substack(profile).model_dump()


async def get_my_notes(token: str, cursor: str | None = None) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        page = await NotesService(publication, substack).get_own_notes(cursor=cursor)
    return NotesPageResponse.from_substack(page).model_dump()


async def get_my_posts(
    token: str, limit: int = 25, cursor: str | None = None
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        profile = await ProfilesService(substack).get_own_profile()
        page = await PostsService(publication, substack).get_posts_for_profile(
            profile.id, limit=limit, cursor=cursor
        )
    return PostsPageResponse.from_substack(page).model_dump()
