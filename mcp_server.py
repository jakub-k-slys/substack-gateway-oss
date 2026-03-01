from __future__ import annotations

import base64
import contextlib
from collections.abc import AsyncGenerator
from typing import Any

from fastmcp import FastMCP
from pydantic import ValidationError
from starlette.responses import JSONResponse

from client.substack import SubstackClient
from converters.markdown import markdown_to_draft_body
from models.schemas import (
    BearerCredentials,
    CommentsResponse,
    CreateDraftResponse,
    CreateNoteResponse,
    DraftResponse,
    FollowingResponse,
    FullPostResponse,
    NoteResponse,
    NotesPageResponse,
    PostsPageResponse,
    ProfileResponse,
)
from models.substack import SubstackUpdateDraftPayload

mcp = FastMCP("substack-gateway")


@contextlib.asynccontextmanager
async def _make_client(
    token: str, publication_url: str
) -> AsyncGenerator[SubstackClient, None]:
    """Decode a base64 Bearer token and yield an authenticated SubstackClient."""
    raw = token.removeprefix("Bearer ").strip()
    try:
        decoded = base64.b64decode(raw).decode()
        creds = BearerCredentials.model_validate_json(decoded)
    except (ValidationError, Exception) as exc:
        raise ValueError(
            "Invalid token: expected base64-encoded JSON credentials"
        ) from exc
    if not creds.substack_sid or not creds.connect_sid:
        raise ValueError("Token must contain substack_sid and connect_sid")
    async with SubstackClient(
        substack_sid=creds.substack_sid,
        connect_sid=creds.connect_sid,
        publication_url=publication_url,
    ) as client:
        yield client


# ------------------------------------------------------------------
# Notes
# ------------------------------------------------------------------


@mcp.tool()
async def get_note(note_id: int, token: str, publication_url: str) -> dict[str, Any]:
    """Get a Substack note by ID."""
    async with _make_client(token, publication_url) as client:
        note = await client.get_note_by_id(note_id)
        return NoteResponse.from_substack(note).model_dump()


@mcp.tool()
async def create_note(
    content: str,
    token: str,
    publication_url: str,
    attachment: str | None = None,
) -> dict[str, Any]:
    """Publish a new Substack note from Markdown content."""
    async with _make_client(token, publication_url) as client:
        note = await client.create_note(content, attachment=attachment)
        return CreateNoteResponse.from_substack(note).model_dump()


@mcp.tool()
async def delete_note(note_id: int, token: str, publication_url: str) -> str:
    """Delete a Substack note by ID."""
    async with _make_client(token, publication_url) as client:
        await client.delete_note(note_id)
        return f"Note {note_id} deleted successfully."


# ------------------------------------------------------------------
# Drafts
# ------------------------------------------------------------------


@mcp.tool()
async def get_draft(draft_id: int, token: str, publication_url: str) -> dict[str, Any]:
    """Get a Substack post draft by ID. Body is returned as Markdown."""
    async with _make_client(token, publication_url) as client:
        draft = await client.get_draft(draft_id)
        return DraftResponse.from_substack(draft).model_dump()


@mcp.tool()
async def create_draft(
    token: str,
    publication_url: str,
    title: str | None = None,
    subtitle: str | None = None,
    body: str | None = None,
) -> dict[str, Any]:
    """Create a new Substack post draft. Body accepts Markdown."""
    async with _make_client(token, publication_url) as client:
        draft = await client.create_draft(title=title, subtitle=subtitle, body=body)
        return CreateDraftResponse.from_substack(draft).model_dump()


@mcp.tool()
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
    async with _make_client(token, publication_url) as client:
        draft = await client.update_draft(
            draft_id, SubstackUpdateDraftPayload(**kwargs)
        )
        return DraftResponse.from_substack(draft).model_dump()


@mcp.tool()
async def delete_draft(draft_id: int, token: str, publication_url: str) -> str:
    """Delete a Substack post draft by ID."""
    async with _make_client(token, publication_url) as client:
        await client.delete_draft(draft_id)
        return f"Draft {draft_id} deleted successfully."


# ------------------------------------------------------------------
# Me
# ------------------------------------------------------------------


@mcp.tool()
async def get_me(token: str, publication_url: str) -> dict[str, Any]:
    """Get the authenticated user's own Substack profile."""
    async with _make_client(token, publication_url) as client:
        profile = await client.get_own_profile()
        return ProfileResponse.from_substack(profile).model_dump()


@mcp.tool()
async def get_my_notes(
    token: str, publication_url: str, cursor: str | None = None
) -> dict[str, Any]:
    """Get the authenticated user's notes (paginated, optional cursor)."""
    async with _make_client(token, publication_url) as client:
        page = await client.get_own_notes(cursor=cursor)
        return NotesPageResponse.from_substack(page).model_dump()


@mcp.tool()
async def get_my_posts(
    token: str, publication_url: str, limit: int = 25, offset: int = 0
) -> dict[str, Any]:
    """Get the authenticated user's posts (paginated)."""
    async with _make_client(token, publication_url) as client:
        page = await client.get_own_posts(limit=limit, offset=offset)
        return PostsPageResponse.from_substack(page).model_dump()


@mcp.tool()
async def get_my_following(token: str, publication_url: str) -> dict[str, Any]:
    """Get the list of users the authenticated user follows."""
    async with _make_client(token, publication_url) as client:
        users = await client.get_own_following()
        return FollowingResponse.from_substack(users).model_dump()


# ------------------------------------------------------------------
# Profiles
# ------------------------------------------------------------------


@mcp.tool()
async def get_profile(slug: str, token: str, publication_url: str) -> dict[str, Any]:
    """Get a public Substack profile by handle/slug."""
    async with _make_client(token, publication_url) as client:
        profile = await client.get_profile_by_slug(slug)
        return ProfileResponse.from_substack(profile).model_dump()


@mcp.tool()
async def get_profile_posts(
    slug: str,
    token: str,
    publication_url: str,
    limit: int = 25,
    offset: int = 0,
) -> dict[str, Any]:
    """Get paginated posts for a Substack profile."""
    async with _make_client(token, publication_url) as client:
        profile_id = await client.get_profile_id_by_slug(slug)
        page = await client.get_posts_for_profile(
            profile_id, limit=limit, offset=offset
        )
        return PostsPageResponse.from_substack(page).model_dump()


@mcp.tool()
async def get_profile_notes(
    slug: str,
    token: str,
    publication_url: str,
    cursor: str | None = None,
) -> dict[str, Any]:
    """Get paginated notes for a Substack profile."""
    async with _make_client(token, publication_url) as client:
        profile_id = await client.get_profile_id_by_slug(slug)
        page = await client.get_notes_for_profile(profile_id, cursor=cursor)
        return NotesPageResponse.from_substack(page).model_dump()


# ------------------------------------------------------------------
# Posts
# ------------------------------------------------------------------


@mcp.tool()
async def get_post(post_id: int, token: str, publication_url: str) -> dict[str, Any]:
    """Get a full Substack post by ID."""
    async with _make_client(token, publication_url) as client:
        post = await client.get_post_by_id(post_id)
        return FullPostResponse.from_substack(post).model_dump()


@mcp.tool()
async def get_post_comments(
    post_id: int, token: str, publication_url: str
) -> dict[str, Any]:
    """Get all comments for a Substack post."""
    async with _make_client(token, publication_url) as client:
        comments = await client.get_comments_for_post(post_id)
        return CommentsResponse.from_substack(comments).model_dump()

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})