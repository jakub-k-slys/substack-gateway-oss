from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from mcp.types import ToolAnnotations
from starlette.responses import JSONResponse

from gateway.mcp.deps import get_notes_service, get_posts_service, get_profiles_service
from gateway.models.schemas import (
    CommentsResponse,
    CreateNoteResponse,
    FullPostResponse,
    NotesPageResponse,
    PostsPageResponse,
)
from gateway.services.notes import NotesService
from gateway.services.posts import PostsService
from gateway.services.profiles import ProfilesService
from gateway_pro.converters.markdown import markdown_to_draft_body
from gateway_pro.mcp.deps import get_drafts_service
from gateway_pro.models.schemas import (
    CreateDraftResponse,
    DraftResponse,
    DraftsListResponse,
)
from gateway_pro.models.substack import SubstackUpdateDraftPayload
from gateway_pro.services.drafts import DraftsService


async def create_note(
    content: str,
    notes: NotesService = Depends(get_notes_service),
    attachment: str | None = None,
) -> dict[str, Any]:
    note = await notes.create_note(content, attachment=attachment)
    return CreateNoteResponse.from_substack(note).model_dump()


async def delete_note(
    note_id: int,
    notes: NotesService = Depends(get_notes_service),
) -> str:
    await notes.delete_note(note_id)
    return f"Note {note_id} deleted successfully."


async def list_drafts(
    drafts: DraftsService = Depends(get_drafts_service),
) -> dict[str, Any]:
    result = await drafts.list_drafts()
    return DraftsListResponse.from_substack(result).model_dump()


async def get_draft(
    draft_id: int,
    drafts: DraftsService = Depends(get_drafts_service),
) -> dict[str, Any]:
    draft = await drafts.get_draft(draft_id)
    return DraftResponse.from_substack(draft).model_dump()


async def create_draft(
    drafts: DraftsService = Depends(get_drafts_service),
    title: str | None = None,
    subtitle: str | None = None,
    body: str | None = None,
) -> dict[str, Any]:
    draft = await drafts.create_draft(title=title, subtitle=subtitle, body=body)
    return CreateDraftResponse.from_substack(draft).model_dump()


async def update_draft(
    draft_id: int,
    drafts: DraftsService = Depends(get_drafts_service),
    title: str | None = None,
    subtitle: str | None = None,
    body: str | None = None,
) -> dict[str, Any]:
    kwargs: dict[str, str] = {}
    if title is not None:
        kwargs["draft_title"] = title
    if subtitle is not None:
        kwargs["draft_subtitle"] = subtitle
    if body is not None:
        kwargs["draft_body"] = markdown_to_draft_body(body)
    draft = await drafts.update_draft(draft_id, SubstackUpdateDraftPayload(**kwargs))
    return DraftResponse.from_substack(draft).model_dump()


async def delete_draft(
    draft_id: int,
    drafts: DraftsService = Depends(get_drafts_service),
) -> str:
    await drafts.delete_draft(draft_id)
    return f"Draft {draft_id} deleted successfully."


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


async def get_profile_notes(
    slug: str,
    profiles: ProfilesService = Depends(get_profiles_service),
    posts: PostsService = Depends(get_posts_service),
    cursor: str | None = None,
) -> dict[str, Any]:
    profile_id = await profiles.get_profile_id_by_slug(slug)
    page = await posts.get_notes_for_profile(profile_id, cursor=cursor)
    return NotesPageResponse.from_substack(page).model_dump()


async def get_post(
    post_id: int,
    posts: PostsService = Depends(get_posts_service),
) -> dict[str, Any]:
    post = await posts.get_post_by_id(post_id)
    return FullPostResponse.from_substack(post).model_dump()


async def get_post_comments(
    post_id: int,
    posts: PostsService = Depends(get_posts_service),
) -> dict[str, Any]:
    comments = await posts.get_comments_for_post(post_id)
    return CommentsResponse.from_substack(comments).model_dump()


async def health_check(request) -> JSONResponse:
    return JSONResponse({"status": "healthy", "service": "mcp-server"})


def register_tools(mcp: FastMCP) -> None:
    mcp.tool(
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
    )(create_note)
    mcp.tool(
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
    )(delete_note)
    mcp.tool(
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
    )(list_drafts)
    mcp.tool(
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
    )(get_draft)
    mcp.tool(
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
    )(create_draft)
    mcp.tool(
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
    )(update_draft)
    mcp.tool(
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
    )(delete_draft)
    mcp.tool(
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
    )(get_profile_posts)
    mcp.tool(
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
    )(get_profile_notes)
    mcp.tool(
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
    )(get_post)
    mcp.tool(
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
    )(get_post_comments)


def register_routes(mcp: FastMCP) -> None:
    mcp.custom_route("/health", methods=["GET"])(health_check)
