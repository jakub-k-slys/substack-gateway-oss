from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = (
    "mcp:stats:subscribers",
    "mcp:stats:traffic:30d-views",
    "mcp:posts:stats:engagement",
    "mcp:posts:stats:traffic",
    "mcp:posts:stats:recipients",
    "mcp:posts:stats:growth",
    "mcp:posts:stats:discussion",
)


def _register(mcp: FastMCP) -> None:
    from gateway_stats_mcp.tools import (
        get_30d_views,
        get_post_discussion,
        get_post_engagement,
        get_post_growth,
        get_post_recipients,
        get_post_traffic,
        get_subscriber_timeseries,
    )

    mcp.tool(
        description="Fetch the publication's daily subscriber timeseries (paid, comps, free trials, total) for the trailing year. Optionally pass `from_date` (ISO) to bound the window. Results are delta-cached: repeat calls only fetch new days from Substack. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"stats", "read"},
        annotations=ToolAnnotations(
            title="Get Subscriber Timeseries",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "stats",
            "substack_endpoint": "GET /publication/stats/subscribers/timeseries",
        },
    )(get_subscriber_timeseries)
    mcp.tool(
        description="Fetch the publication's trailing-30-day view count and its delta versus the prior period. Result is a short-lived cached snapshot. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"stats", "read"},
        annotations=ToolAnnotations(
            title="Get 30-Day Views",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "stats",
            "substack_endpoint": (
                "GET /publication/stats/publication_traffic/30d_views"
            ),
        },
    )(get_30d_views)
    mcp.tool(
        description="Fetch engagement for a published post: like count and likers, comment count and summary, and commenter count. Result is a short-lived cached snapshot. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"post-stats", "read"},
        annotations=ToolAnnotations(
            title="Get Post Engagement",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "post-stats",
            "substack_endpoint": "GET /post_management/detail/{id}/engagement",
        },
    )(get_post_engagement)
    mcp.tool(
        description="Fetch traffic for a published post: view counts broken down by referrer source, device type, and category. Result is a short-lived cached snapshot. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"post-stats", "read"},
        annotations=ToolAnnotations(
            title="Get Post Traffic",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "post-stats",
            "substack_endpoint": "GET /post_management/detail/{id}/traffic",
        },
    )(get_post_traffic)
    mcp.tool(
        description="Fetch per-recipient email stats for a published post (delivery, opens, clicks), paginated via limit/offset. Result is a short-lived cached snapshot. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"post-stats", "read"},
        annotations=ToolAnnotations(
            title="Get Post Recipients",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "post-stats",
            "substack_endpoint": "GET /post_management/detail/{id}/recipients",
        },
    )(get_post_recipients)
    mcp.tool(
        description="Fetch subscriber growth attributed to a published post. Result is a short-lived cached snapshot. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"post-stats", "read"},
        annotations=ToolAnnotations(
            title="Get Post Growth",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "post-stats",
            "substack_endpoint": "GET /post_management/detail/{id}/growth",
        },
    )(get_post_growth)
    mcp.tool(
        description="Fetch the discussion (comment thread) for a published post, cursor-paginated. Result is a short-lived cached snapshot. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"post-stats", "read"},
        annotations=ToolAnnotations(
            title="Get Post Discussion",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "post-stats",
            "substack_endpoint": "GET /post_management/detail/{id}/discussion",
        },
    )(get_post_discussion)


def capability() -> McpCapability:
    return McpCapability(domain="stats", register=_register, features=_FEATURES)
