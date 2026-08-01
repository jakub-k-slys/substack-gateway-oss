from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = ("mcp:me:following:list",)


def _register(mcp: FastMCP) -> None:
    from gateway_following_mcp.tools import get_my_following

    mcp.tool(
        description="Retrieve the list of Substack profiles that the authenticated user follows using an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"me", "following", "read"},
        annotations=ToolAnnotations(
            title="Get My Following",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "me", "substack_endpoint": "GET /user/{id}/subscriber-lists"},
    )(get_my_following)


def capability() -> McpCapability:
    return McpCapability(domain="following", register=_register, features=_FEATURES)
