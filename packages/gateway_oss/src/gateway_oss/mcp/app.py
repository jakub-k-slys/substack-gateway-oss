from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from mcp.types import ToolAnnotations

from gateway_oss.extensions.runtime import get_runtime
from gateway_oss.mcp.deps import (
    get_following_service,
    get_notes_service,
    get_posts_service,
    get_profiles_service,
)
from gateway_oss.models.schemas import (
    CommentsResponse,
    CreateNoteResponse,
    FollowingResponse,
    FullPostResponse,
    NoteResponse,
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)
from gateway_oss.services.following import FollowingService
from gateway_oss.services.notes import NotesService
from gateway_oss.services.posts import PostsService
from gateway_oss.services.profiles import ProfilesService

runtime = get_runtime()

_mcp = FastMCP("substack-gateway", auth=runtime.mcp_auth_provider)


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
    description="Publish a new note to Substack from Markdown content, with an optional link attachment.",
    tags={"notes", "write"},
    annotations=ToolAnnotations(
        title="Create Note",
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
        openWorldHint=True,
    ),
    meta={"category": "notes", "substack_endpoint": "POST /comment/feed/"},
)
async def create_note(
    content: str,
    notes: NotesService = Depends(get_notes_service),
    attachment: str | None = None,
) -> dict[str, Any]:
    note = await notes.create_note(content, attachment=attachment)
    return CreateNoteResponse.from_substack(note).model_dump()


@_mcp.tool(
    description="Permanently delete a Substack note by its numeric ID.",
    tags={"notes", "write", "delete"},
    annotations=ToolAnnotations(
        title="Delete Note",
        readOnlyHint=False,
        destructiveHint=True,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "notes", "substack_endpoint": "DELETE /comment/{note_id}"},
)
async def delete_note(
    note_id: int,
    notes: NotesService = Depends(get_notes_service),
) -> str:
    await notes.delete_note(note_id)
    return f"Note {note_id} deleted successfully."


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
    description="Retrieve the full content of a Substack post by its numeric ID.",
    tags={"posts", "read"},
    annotations=ToolAnnotations(
        title="Get Post",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "posts", "substack_endpoint": "GET /posts/by-id/{post_id}"},
)
async def get_post(
    post_id: int,
    posts: PostsService = Depends(get_posts_service),
) -> dict[str, Any]:
    post = await posts.get_post_by_id(post_id)
    return FullPostResponse.from_substack(post).model_dump()


@_mcp.tool(
    description="Retrieve all comments for a Substack post by its numeric ID.",
    tags={"posts", "comments", "read"},
    annotations=ToolAnnotations(
        title="Get Post Comments",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "posts", "substack_endpoint": "GET /post/{post_id}/comments"},
)
async def get_post_comments(
    post_id: int,
    posts: PostsService = Depends(get_posts_service),
) -> dict[str, Any]:
    comments = await posts.get_comments_for_post(post_id)
    return CommentsResponse.from_substack(comments).model_dump()


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
    profiles: ProfilesService = Depends(get_profiles_service),
    posts: PostsService = Depends(get_posts_service),
    limit: int = 25,
    offset: int = 0,
) -> dict[str, Any]:
    profile_id = await profiles.get_profile_id_by_slug(slug)
    page = await posts.get_posts_for_profile(profile_id, limit=limit, offset=offset)
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
    profiles: ProfilesService = Depends(get_profiles_service),
    posts: PostsService = Depends(get_posts_service),
    cursor: str | None = None,
) -> dict[str, Any]:
    profile_id = await profiles.get_profile_id_by_slug(slug)
    page = await posts.get_notes_for_profile(profile_id, cursor=cursor)
    return NotesPageResponse.from_substack(page).model_dump()


for extension in runtime.extensions:
    extension.register_mcp(_mcp, runtime.context)


mcp = _mcp.http_app(transport="streamable-http", path="/", stateless_http=True)
