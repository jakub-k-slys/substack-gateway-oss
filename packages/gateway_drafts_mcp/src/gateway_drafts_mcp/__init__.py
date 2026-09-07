from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = (
    "mcp:drafts:list",
    "mcp:drafts:get",
    "mcp:drafts:create",
    "mcp:drafts:update",
    "mcp:drafts:delete",
    "mcp:drafts:schedule",
    "mcp:drafts:unschedule",
    "mcp:drafts:prepublish",
    "mcp:drafts:ai-detection",
    "mcp:images:upload",
)


def _register(mcp: FastMCP) -> None:
    from gateway_drafts_mcp.tools import (
        check_draft,
        create_draft,
        delete_draft,
        get_ai_detection,
        get_draft,
        list_drafts,
        schedule_draft,
        unschedule_draft,
        update_draft,
        upload_image,
    )

    mcp.tool(
        description="List Substack post drafts for the publication, newest first, in pages of 10 with cursor-based pagination. Pass `next` from a previous response to fetch the following page. Each item contains id, uuid, title, and last-updated timestamp. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"drafts", "read"},
        annotations=ToolAnnotations(
            title="List Drafts",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "drafts", "substack_endpoint": "GET /post_management/drafts"},
    )(list_drafts)
    mcp.tool(
        description="Fetch a Substack post draft by ID. The body is returned as Markdown. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
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
        description="Create a new Substack post draft with optional title, subtitle, and body. The body accepts Markdown. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
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
        description="Upload an image to Substack and get back its hosted URL and pixel dimensions. Pass the image as base64 in `image_base64` with its `content_type` (e.g. image/png). Reference the returned URL in a draft body as ![alt](url). Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"drafts", "images", "write"},
        annotations=ToolAnnotations(
            title="Upload Image",
            readOnlyHint=False,
            destructiveHint=False,
            idempotentHint=False,
            openWorldHint=True,
        ),
        meta={"category": "drafts", "substack_endpoint": "POST /api/v1/image"},
    )(upload_image)
    mcp.tool(
        description="Update specific fields of a Substack post draft. Only provided fields are changed; omitted fields remain unchanged. Body accepts Markdown. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
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
        description="Permanently delete a Substack post draft by its numeric ID. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
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
        description="Run Substack's Pangram AI-writing detection on a draft. Returns fraction_ai / fraction_ai_assisted / fraction_human plus a human-readable header and details. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"drafts", "read"},
        annotations=ToolAnnotations(
            title="Get AI Detection",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "drafts",
            "substack_endpoint": "GET /drafts/{draft_id}/pangram_detection",
        },
    )(get_ai_detection)
    mcp.tool(
        description="Run Substack's pre-publish validation on a draft, returning any blocking errors and non-blocking suggestions. Call before scheduling. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"drafts", "read"},
        annotations=ToolAnnotations(
            title="Check Draft",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "drafts",
            "substack_endpoint": "GET /drafts/{draft_id}/prepublish",
        },
    )(check_draft)
    mcp.tool(
        description="Schedule a Substack draft for timed release. `scheduled_at` is an ISO-8601 timestamp (UTC recommended, e.g. 2026-09-16T18:24:00Z). `post_audience` and `email_audience` default to only_paid. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"drafts", "write"},
        annotations=ToolAnnotations(
            title="Schedule Draft",
            readOnlyHint=False,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "drafts",
            "substack_endpoint": "POST /drafts/{draft_id}/scheduled_release",
        },
    )(schedule_draft)
    mcp.tool(
        description="Cancel a Substack draft's scheduled release, returning it to an unscheduled draft. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"drafts", "write", "delete"},
        annotations=ToolAnnotations(
            title="Unschedule Draft",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "drafts",
            "substack_endpoint": "DELETE /drafts/{draft_id}/scheduled_release",
        },
    )(unschedule_draft)


def capability() -> McpCapability:
    return McpCapability(domain="drafts", register=_register, features=_FEATURES)
