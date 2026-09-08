from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = (
    "mcp:posts:get",
    "mcp:posts:like",
    "mcp:posts:unlike",
    "mcp:posts:restack",
)


def _register(mcp: FastMCP) -> None:
    from gateway_posts_mcp.tools import get_post, like_post, restack_post, unlike_post

    mcp.tool(
        description="Retrieve the full content of a Substack post by its numeric ID. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"posts", "read"},
        annotations=ToolAnnotations(
            title="Get Post",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={"category": "posts", "substack_endpoint": "GET /posts/by-id/{post_id}"},
    )(get_post)
    mcp.tool(
        description="Add a heart like to a Substack post by its numeric ID. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"posts", "write"},
        annotations=ToolAnnotations(
            title="Like Post",
            read_only_hint=False,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "posts",
            "substack_endpoint": "PUT /posts/{post_id}/like",
        },
    )(like_post)
    mcp.tool(
        description="Remove a heart like from a Substack post by its numeric ID. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"posts", "write", "delete"},
        annotations=ToolAnnotations(
            title="Unlike Post",
            read_only_hint=False,
            destructive_hint=True,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "posts",
            "substack_endpoint": "DELETE /posts/{post_id}/like",
        },
    )(unlike_post)
    mcp.tool(
        description="Restack a Substack post into the authenticated user's feed by its numeric ID. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"posts", "write"},
        annotations=ToolAnnotations(
            title="Restack Post",
            read_only_hint=False,
            destructive_hint=False,
            idempotent_hint=False,
            open_world_hint=True,
        ),
        meta={
            "category": "posts",
            "substack_endpoint": "POST /posts/{post_id}/restack",
        },
    )(restack_post)


def capability() -> McpCapability:
    return McpCapability(domain="posts", register=_register, features=_FEATURES)
