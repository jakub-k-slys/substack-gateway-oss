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
        description="List Substack post drafts for the publication, newest first, in pages of 10 with cursor-based pagination. Pass `next` from a previous response to fetch the following page. Each item contains id, uuid, title, and last-updated timestamp. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"drafts", "read"},
        annotations=ToolAnnotations(
            title="List Drafts",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={"category": "drafts", "substack_endpoint": "GET /post_management/drafts"},
    )(list_drafts)
    mcp.tool(
        description="Fetch a Substack post draft by ID. The body is returned as Markdown. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"drafts", "read"},
        annotations=ToolAnnotations(
            title="Get Draft",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={"category": "drafts", "substack_endpoint": "GET /drafts/{draft_id}"},
    )(get_draft)
    mcp.tool(
        description="Create a new Substack post draft with optional title, subtitle, and body. The body accepts Markdown. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"drafts", "write"},
        annotations=ToolAnnotations(
            title="Create Draft",
            read_only_hint=False,
            destructive_hint=False,
            idempotent_hint=False,
            open_world_hint=True,
        ),
        meta={"category": "drafts", "substack_endpoint": "POST /drafts"},
    )(create_draft)
    mcp.tool(
        description="Upload an image to Substack and get back its hosted URL and pixel dimensions. Pass the image as base64 in `image_base64` with its `content_type` (e.g. image/png). Reference the returned URL in a draft body as ![alt](url). The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"drafts", "images", "write"},
        annotations=ToolAnnotations(
            title="Upload Image",
            read_only_hint=False,
            destructive_hint=False,
            idempotent_hint=False,
            open_world_hint=True,
        ),
        meta={"category": "drafts", "substack_endpoint": "POST /api/v1/image"},
    )(upload_image)
    mcp.tool(
        description="Update specific fields of a Substack post draft. Only provided fields are changed; omitted fields remain unchanged. Body accepts Markdown. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"drafts", "write"},
        annotations=ToolAnnotations(
            title="Update Draft",
            read_only_hint=False,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={"category": "drafts", "substack_endpoint": "PUT /drafts/{draft_id}"},
    )(update_draft)
    mcp.tool(
        description="Permanently delete a Substack post draft by its numeric ID. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"drafts", "write", "delete"},
        annotations=ToolAnnotations(
            title="Delete Draft",
            read_only_hint=False,
            destructive_hint=True,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={"category": "drafts", "substack_endpoint": "DELETE /drafts/{draft_id}"},
    )(delete_draft)
    mcp.tool(
        description="Run Substack's Pangram AI-writing detection on a draft. Returns fraction_ai / fraction_ai_assisted / fraction_human plus a human-readable header and details. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"drafts", "read"},
        annotations=ToolAnnotations(
            title="Get AI Detection",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "drafts",
            "substack_endpoint": "GET /drafts/{draft_id}/pangram_detection",
        },
    )(get_ai_detection)
    mcp.tool(
        description="Run Substack's pre-publish validation on a draft, returning any blocking errors and non-blocking suggestions. Call before scheduling. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"drafts", "read"},
        annotations=ToolAnnotations(
            title="Check Draft",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "drafts",
            "substack_endpoint": "GET /drafts/{draft_id}/prepublish",
        },
    )(check_draft)
    mcp.tool(
        description="Schedule a Substack draft for timed release. `scheduled_at` is an ISO-8601 timestamp (UTC recommended, e.g. 2026-09-16T18:24:00Z). `post_audience` and `email_audience` default to only_paid. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"drafts", "write"},
        annotations=ToolAnnotations(
            title="Schedule Draft",
            read_only_hint=False,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "drafts",
            "substack_endpoint": "POST /drafts/{draft_id}/scheduled_release",
        },
    )(schedule_draft)
    mcp.tool(
        description="Cancel a Substack draft's scheduled release, returning it to an unscheduled draft. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"drafts", "write", "delete"},
        annotations=ToolAnnotations(
            title="Unschedule Draft",
            read_only_hint=False,
            destructive_hint=True,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "drafts",
            "substack_endpoint": "DELETE /drafts/{draft_id}/scheduled_release",
        },
    )(unschedule_draft)


def capability() -> McpCapability:
    return McpCapability(domain="drafts", register=_register, features=_FEATURES)
