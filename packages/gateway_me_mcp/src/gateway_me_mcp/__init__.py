from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = ("mcp:me:get", "mcp:me:notes:list", "mcp:me:posts:list")


def _register(mcp: FastMCP) -> None:
    from gateway_me_mcp.tools import get_me, get_my_notes, get_my_posts

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


def capability() -> McpCapability:
    return McpCapability(domain="me", register=_register, features=_FEATURES)
