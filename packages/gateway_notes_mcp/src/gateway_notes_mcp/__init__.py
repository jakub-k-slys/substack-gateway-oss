from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = ("mcp:notes:get", "mcp:notes:create", "mcp:notes:delete")


def _register(mcp: FastMCP) -> None:
    from gateway_notes_mcp.tools import create_note, delete_note, get_note

    mcp.tool(
        description="Publish a new note to Substack from Markdown content, with an optional link attachment. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
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
        description="Permanently delete a Substack note by its numeric ID. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
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
        description="Retrieve a single Substack note by its numeric ID. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"notes", "read"},
        annotations=ToolAnnotations(
            title="Get Note",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "notes",
            "substack_endpoint": "GET /reader/comment/{note_id}",
        },
    )(get_note)


def capability() -> McpCapability:
    return McpCapability(domain="notes", register=_register, features=_FEATURES)
