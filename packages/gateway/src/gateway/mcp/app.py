from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from mcp.types import ToolAnnotations

from gateway.mcp.deps import (
    get_following_service,
    get_notes_service,
    get_posts_service,
    get_profiles_service,
)
from gateway.models.schemas import (
    FollowingResponse,
    NoteResponse,
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)
from gateway.services.following import FollowingService
from gateway.services.notes import NotesService
from gateway.services.posts import PostsService
from gateway.services.profiles import ProfilesService


def _load_auth_provider():
    try:
        from gateway_pro.oauth.router import oauth_provider
    except ImportError:
        return None
    return oauth_provider


try:
    from gateway_pro.mcp import app as _pro_mcp
except ImportError:
    register_pro_routes = None
    register_pro_tools = None
else:
    create_draft = _pro_mcp.create_draft
    create_note = _pro_mcp.create_note
    delete_draft = _pro_mcp.delete_draft
    delete_note = _pro_mcp.delete_note
    get_draft = _pro_mcp.get_draft
    get_post = _pro_mcp.get_post
    get_post_comments = _pro_mcp.get_post_comments
    get_profile_notes = _pro_mcp.get_profile_notes
    get_profile_posts = _pro_mcp.get_profile_posts
    list_drafts = _pro_mcp.list_drafts
    register_pro_routes = _pro_mcp.register_routes
    register_pro_tools = _pro_mcp.register_tools
    update_draft = _pro_mcp.update_draft


_mcp = FastMCP("substack-gateway", auth=_load_auth_provider())


@_mcp.tool(
    description="Retrieve a single Substack note by its numeric ID.",
    tags={"notes", "read"},
    annotations=ToolAnnotations(
        title="Get Note",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "notes", "substack_endpoint": "GET /reader/comment/{note_id}"},
)
async def get_note(
    note_id: int,
    notes: NotesService = Depends(get_notes_service),
) -> dict[str, Any]:
    note = await notes.get_note_by_id(note_id)
    return NoteResponse.from_substack(note).model_dump()


@_mcp.tool(
    description="Retrieve the authenticated user's own Substack public profile.",
    tags={"me", "profile", "read"},
    annotations=ToolAnnotations(
        title="Get My Profile",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "me", "substack_endpoint": "GET /user/{slug}/public_profile"},
)
async def get_me(
    profiles: ProfilesService = Depends(get_profiles_service),
) -> dict[str, Any]:
    profile = await profiles.get_own_profile()
    return ProfileResponse.from_substack(profile).model_dump()


@_mcp.tool(
    description="Retrieve the authenticated user's own notes, paginated via an optional cursor.",
    tags={"me", "notes", "read"},
    annotations=ToolAnnotations(
        title="Get My Notes",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "me", "substack_endpoint": "GET /notes"},
)
async def get_my_notes(
    notes: NotesService = Depends(get_notes_service),
    cursor: str | None = None,
) -> dict[str, Any]:
    page = await notes.get_own_notes(cursor=cursor)
    return NotesPageResponse.from_substack(page).model_dump()


@_mcp.tool(
    description="Retrieve the authenticated user's own posts, paginated via limit and offset.",
    tags={"me", "posts", "read"},
    annotations=ToolAnnotations(
        title="Get My Posts",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "me", "substack_endpoint": "GET /profile/posts"},
)
async def get_my_posts(
    profiles: ProfilesService = Depends(get_profiles_service),
    posts: PostsService = Depends(get_posts_service),
    limit: int = 25,
    offset: int = 0,
) -> dict[str, Any]:
    profile = await profiles.get_own_profile()
    page = await posts.get_posts_for_profile(profile.id, limit=limit, offset=offset)
    return PostsPageResponse.from_substack(page).model_dump()


@_mcp.tool(
    description="Retrieve the list of Substack profiles that the authenticated user follows.",
    tags={"me", "following", "read"},
    annotations=ToolAnnotations(
        title="Get My Following",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "me", "substack_endpoint": "GET /user/{id}/subscriber-lists"},
)
async def get_my_following(
    following: FollowingService = Depends(get_following_service),
) -> dict[str, Any]:
    users = await following.get_own_following()
    return FollowingResponse.from_substack(users).model_dump()


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
    profiles: ProfilesService = Depends(get_profiles_service),
) -> dict[str, Any]:
    profile = await profiles.get_profile_by_slug(slug)
    return ProfileResponse.from_substack(profile).model_dump()


if register_pro_tools is not None:
    register_pro_tools(_mcp)

if register_pro_routes is not None:
    register_pro_routes(_mcp)


mcp = _mcp.http_app(transport="streamable-http", path="/", stateless_http=True)
