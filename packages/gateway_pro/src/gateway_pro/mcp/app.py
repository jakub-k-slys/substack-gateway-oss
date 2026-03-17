from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from mcp.types import ToolAnnotations
from starlette.responses import JSONResponse

from gateway_pro.converters.markdown import markdown_to_draft_body
from gateway_pro.mcp.deps import get_drafts_service
from gateway_pro.models.schemas import (
    CreateDraftResponse,
    DraftResponse,
    DraftsListResponse,
)
from gateway_pro.models.substack import SubstackUpdateDraftPayload
from gateway_pro.services.drafts import DraftsService


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


async def health_check(request) -> JSONResponse:
    return JSONResponse({"status": "healthy", "service": "mcp-server"})


def register_tools(mcp: FastMCP) -> None:
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


def register_routes(mcp: FastMCP) -> None:
    mcp.custom_route("/health", methods=["GET"])(health_check)
