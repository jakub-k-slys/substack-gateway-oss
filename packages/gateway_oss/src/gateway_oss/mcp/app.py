from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from gateway_mcp_common.clients import (
    _anonymous_credentials,  # noqa: F401
    _authenticated_clients,
    _public_publication_client,
    _public_substack_client,
)
from gateway_oss.extensions.runtime import get_runtime
from gateway_oss.models.schemas import (
    CommentsResponse,
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)
from gateway_oss.services.notes import NotesService
from gateway_oss.services.posts import PostsService
from gateway_oss.services.profiles import ProfilesService

runtime = get_runtime()

_mcp = FastMCP("substack-gateway", auth=runtime.mcp_auth_provider)


async def get_me(
    token: str,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (_publication, substack):
        profile = await ProfilesService(substack).get_own_profile()
    return ProfileResponse.from_substack(profile).model_dump()


async def get_my_notes(
    token: str,
    cursor: str | None = None,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        page = await NotesService(publication, substack).get_own_notes(cursor=cursor)
    return NotesPageResponse.from_substack(page).model_dump()


async def get_my_posts(
    token: str,
    limit: int = 25,
    cursor: str | None = None,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        profiles = ProfilesService(substack)
        posts = PostsService(publication, substack)
        profile = await profiles.get_own_profile()
        page = await posts.get_posts_for_profile(profile.id, limit=limit, cursor=cursor)
    return PostsPageResponse.from_substack(page).model_dump()


async def get_post_comments(
    post_id: int,
    token: str,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        comments = await PostsService(publication, substack).get_comments_for_post(
            post_id
        )
    return CommentsResponse.from_substack(comments).model_dump()


@_mcp.tool(
    description="Retrieve a public Substack profile by its handle/slug.",
    tags={"profiles", "read"},
    annotations=ToolAnnotations(
        title="Get Profile",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={
        "category": "profiles",
        "substack_endpoint": "GET /user/{slug}/public_profile",
    },
)
async def get_profile(
    slug: str,
) -> dict[str, Any]:
    async with _public_substack_client() as substack:
        profile = await ProfilesService(substack).get_profile_by_slug(slug)
    return ProfileResponse.from_substack(profile).model_dump()


@_mcp.tool(
    description="Retrieve a paginated list of posts for a Substack profile identified by handle/slug.",
    tags={"profiles", "posts", "read"},
    annotations=ToolAnnotations(
        title="Get Profile Posts",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "profiles", "substack_endpoint": "GET /profile/posts"},
)
async def get_profile_posts(
    slug: str,
    limit: int = 25,
    cursor: str | None = None,
) -> dict[str, Any]:
    async with (
        _public_publication_client() as publication,
        _public_substack_client() as substack,
    ):
        profiles = ProfilesService(substack)
        posts = PostsService(publication, substack)
        profile_id = await profiles.get_profile_id_by_slug(slug)
        page = await posts.get_posts_for_profile(profile_id, limit=limit, cursor=cursor)
    return PostsPageResponse.from_substack(page).model_dump()


@_mcp.tool(
    description="Retrieve a paginated list of notes for a Substack profile identified by handle/slug.",
    tags={"profiles", "notes", "read"},
    annotations=ToolAnnotations(
        title="Get Profile Notes",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={
        "category": "profiles",
        "substack_endpoint": "GET /reader/feed/profile/{id}",
    },
)
async def get_profile_notes(
    slug: str,
    cursor: str | None = None,
) -> dict[str, Any]:
    async with (
        _public_publication_client() as publication,
        _public_substack_client() as substack,
    ):
        profiles = ProfilesService(substack)
        posts = PostsService(publication, substack)
        profile_id = await profiles.get_profile_id_by_slug(slug)
        page = await posts.get_notes_for_profile(profile_id, cursor=cursor)
    return NotesPageResponse.from_substack(page).model_dump()


def register_authenticated_tools(mcp: FastMCP) -> None:
    mcp.tool(
        description="Retrieve the authenticated user's own Substack public profile using an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"me", "profile", "read"},
        annotations=ToolAnnotations(
            title="Get My Profile",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /user/{slug}/public_profile"},
    )(get_me)
    mcp.tool(
        description="Retrieve the authenticated user's own notes, paginated via an optional cursor. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"me", "notes", "read"},
        annotations=ToolAnnotations(
            title="Get My Notes",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /notes"},
    )(get_my_notes)
    mcp.tool(
        description="Retrieve the authenticated user's own posts, paginated via limit and offset. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"me", "posts", "read"},
        annotations=ToolAnnotations(
            title="Get My Posts",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /profile/posts"},
    )(get_my_posts)
    mcp.tool(
        description="Retrieve all comments for a Substack post by its numeric ID. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"posts", "comments", "read"},
        annotations=ToolAnnotations(
            title="Get Post Comments",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "posts",
            "substack_endpoint": "GET /post/{post_id}/comments",
        },
    )(get_post_comments)


_mcp_app: Any = None


def _build_mcp_app() -> Any:
    from gateway_oss.registry import load_mcp_capabilities

    for cap in load_mcp_capabilities():
        cap.register(_mcp)
    for extension in runtime.extensions:
        extension.register_mcp(_mcp, runtime.context)
    return _mcp.http_app(transport="streamable-http", path="/", stateless_http=True)


def __getattr__(name: str) -> Any:
    # Build the MCP ASGI app lazily: extension registration must not run at
    # import time. An extension's register_mcp imports gateway_pro.mcp.app,
    # which imports this module back — doing that during import would re-enter
    # a partially-initialised module and raise a circular ImportError.
    if name == "mcp":
        global _mcp_app
        if _mcp_app is None:
            _mcp_app = _build_mcp_app()
        return _mcp_app
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
