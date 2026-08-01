from __future__ import annotations

from typing import Any

from gateway_mcp_common.clients import (
    _public_publication_client,
    _public_substack_client,
)
from gateway_notes.schemas import NotesPageResponse
from gateway_notes.service import NotesService
from gateway_posts.schemas import PostsPageResponse
from gateway_posts.service import PostsService
from gateway_profiles.schemas import ProfileResponse
from gateway_profiles.service import ProfilesService


async def get_profile(slug: str) -> dict[str, Any]:
    async with _public_substack_client() as substack:
        profile = await ProfilesService(substack).get_profile_by_slug(slug)
    return ProfileResponse.from_substack(profile).model_dump()


async def get_profile_posts(
    slug: str, limit: int = 25, cursor: str | None = None
) -> dict[str, Any]:
    async with (
        _public_publication_client() as publication,
        _public_substack_client() as substack,
    ):
        profile_id = await ProfilesService(substack).get_profile_id_by_slug(slug)
        page = await PostsService(publication, substack).get_posts_for_profile(
            profile_id, limit=limit, cursor=cursor
        )
    return PostsPageResponse.from_substack(page).model_dump()


async def get_profile_notes(slug: str, cursor: str | None = None) -> dict[str, Any]:
    async with (
        _public_publication_client() as publication,
        _public_substack_client() as substack,
    ):
        profile_id = await ProfilesService(substack).get_profile_id_by_slug(slug)
        page = await NotesService(publication, substack).get_notes_for_profile(
            profile_id, cursor=cursor
        )
    return NotesPageResponse.from_substack(page).model_dump()
