from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = ("mcp:posts:get",)


def _register(mcp: FastMCP) -> None:
    from gateway_posts_mcp.tools import get_post

    mcp.tool(
        description="Retrieve the full content of a Substack post by its numeric ID. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
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


def capability() -> McpCapability:
    return McpCapability(domain="posts", register=_register, features=_FEATURES)
