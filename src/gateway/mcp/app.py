from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from starlette.responses import JSONResponse

from gateway.auth import (
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway.client.publication import PublicationClient
from gateway.client.substack import SubstackClient
from gateway.converters.markdown import markdown_to_draft_body
from gateway.models.schemas import (
    CommentsResponse,
    CreateDraftResponse,
    CreateNoteResponse,
    DraftResponse,
    DraftsListResponse,
    FollowingResponse,
    FullPostResponse,
    NoteResponse,
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)
from gateway.models.substack import SubstackUpdateDraftPayload
from gateway.services.drafts import DraftsService
from gateway.services.following import FollowingService
from gateway.services.notes import NotesService
from gateway.services.posts import PostsService
from gateway.services.profiles import ProfilesService

_mcp = FastMCP("substack-gateway")


@contextlib.asynccontextmanager
async def _make_clients(
    token: str, publication_url: str
) -> AsyncIterator[tuple[PublicationClient, SubstackClient]]:
    """Decode a base64 Bearer token and yield authenticated pub + sub clients."""
    creds = decode_bearer_credentials(token.removeprefix("Bearer ").strip())
    async with (
        make_publication_client(creds, publication_url) as pub,
        make_substack_client(creds) as sub,
    ):
        yield pub, sub


# ------------------------------------------------------------------
# Notes
# ------------------------------------------------------------------


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
async def get_note(note_id: int, token: str, publication_url: str) -> dict[str, Any]:
    """Get a Substack note by ID."""
    async with _make_clients(token, publication_url) as (pub, sub):
        note = await NotesService(pub, sub).get_note_by_id(note_id)
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
    token: str,
    publication_url: str,
    attachment: str | None = None,
) -> dict[str, Any]:
    """Publish a new Substack note from Markdown content."""
    async with _make_clients(token, publication_url) as (pub, sub):
        note = await NotesService(pub, sub).create_note(content, attachment=attachment)
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
async def delete_note(note_id: int, token: str, publication_url: str) -> str:
    """Delete a Substack note by ID."""
    async with _make_clients(token, publication_url) as (pub, sub):
        await NotesService(pub, sub).delete_note(note_id)
        return f"Note {note_id} deleted successfully."


# ------------------------------------------------------------------
# Drafts
# ------------------------------------------------------------------


@_mcp.tool(
    description="List all Substack post drafts for the publication, returning id, uuid, title, and last-updated timestamp for each.",
    tags={"drafts", "read"},
    annotations=ToolAnnotations(
        title="List Drafts",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "drafts", "substack_endpoint": "GET /drafts"},
)
async def list_drafts(token: str, publication_url: str) -> dict[str, Any]:
    """List all Substack post drafts."""
    async with _make_clients(token, publication_url) as (pub, sub):
        drafts = await DraftsService(pub, sub).list_drafts()
        return DraftsListResponse.from_substack(drafts).model_dump()


@_mcp.tool(
    description="Fetch a Substack post draft by ID. The body is returned as Markdown.",
    tags={"drafts", "read"},
    annotations=ToolAnnotations(
        title="Get Draft",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "drafts", "substack_endpoint": "GET /drafts/{draft_id}"},
)
async def get_draft(draft_id: int, token: str, publication_url: str) -> dict[str, Any]:
    """Get a Substack post draft by ID. Body is returned as Markdown."""
    async with _make_clients(token, publication_url) as (pub, sub):
        draft = await DraftsService(pub, sub).get_draft(draft_id)
        return DraftResponse.from_substack(draft).model_dump()


@_mcp.tool(
    description="Create a new Substack post draft with optional title, subtitle, and body. The body accepts Markdown.",
    tags={"drafts", "write"},
    annotations=ToolAnnotations(
        title="Create Draft",
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
        openWorldHint=True,
    ),
    meta={"category": "drafts", "substack_endpoint": "POST /drafts"},
)
async def create_draft(
    token: str,
    publication_url: str,
    title: str | None = None,
    subtitle: str | None = None,
    body: str | None = None,
) -> dict[str, Any]:
    """Create a new Substack post draft. Body accepts Markdown."""
    async with _make_clients(token, publication_url) as (pub, sub):
        draft = await DraftsService(pub, sub).create_draft(
            title=title, subtitle=subtitle, body=body
        )
        return CreateDraftResponse.from_substack(draft).model_dump()


@_mcp.tool(
    description="Update specific fields of a Substack post draft. Only provided fields are changed; omitted fields remain unchanged. Body accepts Markdown.",
    tags={"drafts", "write"},
    annotations=ToolAnnotations(
        title="Update Draft",
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "drafts", "substack_endpoint": "PUT /drafts/{draft_id}"},
)
async def update_draft(
    draft_id: int,
    token: str,
    publication_url: str,
    title: str | None = None,
    subtitle: str | None = None,
    body: str | None = None,
) -> dict[str, Any]:
    """Update fields of a Substack post draft. Only provided fields are updated. Body accepts Markdown."""
    kwargs: dict[str, str] = {}
    if title is not None:
        kwargs["draft_title"] = title
    if subtitle is not None:
        kwargs["draft_subtitle"] = subtitle
    if body is not None:
        kwargs["draft_body"] = markdown_to_draft_body(body)
    async with _make_clients(token, publication_url) as (pub, sub):
        draft = await DraftsService(pub, sub).update_draft(
            draft_id, SubstackUpdateDraftPayload(**kwargs)
        )
        return DraftResponse.from_substack(draft).model_dump()


@_mcp.tool(
    description="Permanently delete a Substack post draft by its numeric ID.",
    tags={"drafts", "write", "delete"},
    annotations=ToolAnnotations(
        title="Delete Draft",
        readOnlyHint=False,
        destructiveHint=True,
        idempotentHint=True,
        openWorldHint=True,
    ),
    meta={"category": "drafts", "substack_endpoint": "DELETE /drafts/{draft_id}"},
)
async def delete_draft(draft_id: int, token: str, publication_url: str) -> str:
    """Delete a Substack post draft by ID."""
    async with _make_clients(token, publication_url) as (pub, sub):
        await DraftsService(pub, sub).delete_draft(draft_id)
        return f"Draft {draft_id} deleted successfully."


# ------------------------------------------------------------------
# Me
# ------------------------------------------------------------------


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
async def get_me(token: str, publication_url: str) -> dict[str, Any]:
    """Get the authenticated user's own Substack profile."""
    async with _make_clients(token, publication_url) as (pub, sub):
        profile = await ProfilesService(sub).get_own_profile()
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
    token: str, publication_url: str, cursor: str | None = None
) -> dict[str, Any]:
    """Get the authenticated user's notes (paginated, optional cursor)."""
    async with _make_clients(token, publication_url) as (pub, sub):
        page = await NotesService(pub, sub).get_own_notes(cursor=cursor)
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
    token: str, publication_url: str, limit: int = 25, offset: int = 0
) -> dict[str, Any]:
    """Get the authenticated user's posts (paginated)."""
    async with _make_clients(token, publication_url) as (pub, sub):
        profile = await ProfilesService(sub).get_own_profile()
        page = await PostsService(pub, sub).get_posts_for_profile(
            profile.id, limit=limit, offset=offset
        )
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
async def get_my_following(token: str, publication_url: str) -> dict[str, Any]:
    """Get the list of users the authenticated user follows."""
    async with _make_clients(token, publication_url) as (pub, sub):
        users = await FollowingService(pub, sub).get_own_following()
        return FollowingResponse.from_substack(users).model_dump()


# ------------------------------------------------------------------
# Profiles
# ------------------------------------------------------------------


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
async def get_profile(slug: str, token: str, publication_url: str) -> dict[str, Any]:
    """Get a public Substack profile by handle/slug."""
    async with _make_clients(token, publication_url) as (pub, sub):
        profile = await ProfilesService(sub).get_profile_by_slug(slug)
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
    token: str,
    publication_url: str,
    limit: int = 25,
    offset: int = 0,
) -> dict[str, Any]:
    """Get paginated posts for a Substack profile."""
    async with _make_clients(token, publication_url) as (pub, sub):
        profile_id = await ProfilesService(sub).get_profile_id_by_slug(slug)
        page = await PostsService(pub, sub).get_posts_for_profile(
            profile_id, limit=limit, offset=offset
        )
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
    meta={"category": "profiles", "substack_endpoint": "GET /reader/feed/profile/{id}"},
)
async def get_profile_notes(
    slug: str,
    token: str,
    publication_url: str,
    cursor: str | None = None,
) -> dict[str, Any]:
    """Get paginated notes for a Substack profile."""
    async with _make_clients(token, publication_url) as (pub, sub):
        profile_id = await ProfilesService(sub).get_profile_id_by_slug(slug)
        page = await PostsService(pub, sub).get_notes_for_profile(
            profile_id, cursor=cursor
        )
        return NotesPageResponse.from_substack(page).model_dump()


# ------------------------------------------------------------------
# Posts
# ------------------------------------------------------------------


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
async def get_post(post_id: int, token: str, publication_url: str) -> dict[str, Any]:
    """Get a full Substack post by ID."""
    async with _make_clients(token, publication_url) as (pub, sub):
        post = await PostsService(pub, sub).get_post_by_id(post_id)
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
    post_id: int, token: str, publication_url: str
) -> dict[str, Any]:
    """Get all comments for a Substack post."""
    async with _make_clients(token, publication_url) as (pub, sub):
        comments = await PostsService(pub, sub).get_comments_for_post(post_id)
        return CommentsResponse.from_substack(comments).model_dump()


@_mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})


mcp = _mcp.http_app(transport="streamable-http", path="/", stateless_http=True)
