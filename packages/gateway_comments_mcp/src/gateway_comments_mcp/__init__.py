from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = (
    "mcp:posts:comments:list",
    "mcp:comments:create",
    "mcp:comments:reply",
    "mcp:comments:get",
    "mcp:comments:delete",
    "mcp:comments:replies:list",
    "mcp:comments:like",
    "mcp:comments:unlike",
)


def _register(mcp: FastMCP) -> None:
    from gateway_comments_mcp.tools import (
        create_post_comment,
        delete_post_comment,
        get_post_comment,
        get_post_comments,
        like_post_comment,
        list_post_comment_replies,
        reply_to_post_comment,
        unlike_post_comment,
    )

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

    mcp.tool(
        description="Create a top-level comment on a Substack post. Requires an explicit base64-encoded Substack credentials token via the token argument.",
        tags={"comments", "write"},
        annotations=ToolAnnotations(
            title="Create Post Comment",
            readOnlyHint=False,
            destructiveHint=False,
            idempotentHint=False,
            openWorldHint=True,
        ),
        meta={
            "category": "comments",
            "substack_endpoint": "POST /post/{post_id}/comment",
        },
    )(create_post_comment)

    mcp.tool(
        description="Reply to an existing Substack post comment. Requires an explicit base64-encoded Substack credentials token via the token argument.",
        tags={"comments", "write"},
        annotations=ToolAnnotations(
            title="Reply To Post Comment",
            readOnlyHint=False,
            destructiveHint=False,
            idempotentHint=False,
            openWorldHint=True,
        ),
        meta={
            "category": "comments",
            "substack_endpoint": "POST /post/{post_id}/comment",
        },
    )(reply_to_post_comment)

    mcp.tool(
        description="Fetch a single Substack post comment by its numeric ID. Requires an explicit base64-encoded Substack credentials token via the token argument.",
        tags={"comments", "read"},
        annotations=ToolAnnotations(
            title="Get Post Comment",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "comments", "substack_endpoint": "GET /reader/comment/{id}"},
    )(get_post_comment)

    mcp.tool(
        description="Delete a Substack post comment by its numeric ID. Requires an explicit base64-encoded Substack credentials token via the token argument.",
        tags={"comments", "write", "delete"},
        annotations=ToolAnnotations(
            title="Delete Post Comment",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={"category": "comments", "substack_endpoint": "DELETE /comment/{id}"},
    )(delete_post_comment)

    mcp.tool(
        description="List the direct replies to a Substack post comment. Requires an explicit base64-encoded Substack credentials token via the token argument.",
        tags={"comments", "read"},
        annotations=ToolAnnotations(
            title="List Post Comment Replies",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "comments",
            "substack_endpoint": "GET /reader/comment/{id}/replies",
        },
    )(list_post_comment_replies)

    mcp.tool(
        description="Add a like reaction to a Substack post comment. Requires an explicit base64-encoded Substack credentials token via the token argument.",
        tags={"comments", "write"},
        annotations=ToolAnnotations(
            title="Like Post Comment",
            readOnlyHint=False,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "comments",
            "substack_endpoint": "POST /comment/{id}/reaction",
        },
    )(like_post_comment)

    mcp.tool(
        description="Remove your like reaction from a Substack post comment. Requires an explicit base64-encoded Substack credentials token via the token argument.",
        tags={"comments", "write"},
        annotations=ToolAnnotations(
            title="Unlike Post Comment",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=True,
            openWorldHint=True,
        ),
        meta={
            "category": "comments",
            "substack_endpoint": "DELETE /comment/{id}/reaction",
        },
    )(unlike_post_comment)


def capability() -> McpCapability:
    return McpCapability(domain="comments", register=_register, features=_FEATURES)
