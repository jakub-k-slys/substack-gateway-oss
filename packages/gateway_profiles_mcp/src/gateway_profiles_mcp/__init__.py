from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = ("mcp:profiles:get", "mcp:profiles:posts:list", "mcp:profiles:notes:list")


def _register(mcp: FastMCP) -> None:
    from gateway_profiles_mcp.tools import (
        get_profile,
        get_profile_notes,
        get_profile_posts,
    )

    mcp.tool(
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
    )(get_profile)
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
        meta={
            "category": "profiles",
            "substack_endpoint": "GET /reader/feed/profile/{id}",
        },
    )(get_profile_notes)


def capability() -> McpCapability:
    return McpCapability(domain="profiles", register=_register, features=_FEATURES)
