from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = ("mcp:posts:comments:list",)


def _register(mcp: FastMCP) -> None:
    from gateway_comments_mcp.tools import get_post_comments

    mcp.tool(
        description="Retrieve all comments for a Substack post by its numeric ID. Requires an explicit base64-encoded Substack credentials token passed via the tool's token argument.",
        tags={"posts", "comments", "read"},
        annotations=ToolAnnotations(
            title="Get Post Comments",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "posts",
            "substack_endpoint": "GET /post/{post_id}/comments",
        },
    )(get_post_comments)


def capability() -> McpCapability:
    return McpCapability(domain="comments", register=_register, features=_FEATURES)
