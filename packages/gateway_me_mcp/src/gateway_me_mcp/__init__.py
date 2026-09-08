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
        description="Retrieve the authenticated user's own Substack public profile. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"me", "profile", "read"},
        annotations=ToolAnnotations(
            title="Get My Profile",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /user/{slug}/public_profile"},
    )(get_me)
    mcp.tool(
        description="Retrieve the authenticated user's own notes, paginated via an optional cursor. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"me", "notes", "read"},
        annotations=ToolAnnotations(
            title="Get My Notes",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /notes"},
    )(get_my_notes)
    mcp.tool(
        description="Retrieve the authenticated user's own posts, paginated via limit and offset. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"me", "posts", "read"},
        annotations=ToolAnnotations(
            title="Get My Posts",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /profile/posts"},
    )(get_my_posts)


def capability() -> McpCapability:
    return McpCapability(domain="me", register=_register, features=_FEATURES)
