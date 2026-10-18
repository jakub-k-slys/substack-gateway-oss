from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.types import ToolAnnotations

from gateway_core.capabilities import McpCapability

if TYPE_CHECKING:
    from fastmcp import FastMCP

_FEATURES = (
    "mcp:stats:subscribers",
    "mcp:stats:traffic:30d-views",
    "mcp:stats:arr",
    "mcp:stats:emails",
    "mcp:stats:dashboard",
    "mcp:stats:dashboard:period",
    "mcp:stats:recommendations",
    "mcp:stats:post-counts",
    "mcp:posts:stats:engagement",
    "mcp:posts:stats:traffic",
    "mcp:posts:stats:recipients",
    "mcp:posts:stats:growth",
    "mcp:posts:stats:discussion",
)


def _register(mcp: FastMCP) -> None:
    from gateway_stats_mcp.tools import (
        get_30d_views,
        get_arr_timeseries,
        get_dashboard_period,
        get_dashboard_summary,
        get_email_timeseries,
        get_post_counts,
        get_post_discussion,
        get_post_engagement,
        get_post_growth,
        get_post_recipients,
        get_post_traffic,
        get_recommendation_stats,
        get_subscriber_timeseries,
    )

    mcp.tool(
        description="Fetch the publication's daily subscriber timeseries (paid, comps, free trials, total) for the trailing 7 days by default. Optionally pass `from_date` (ISO) to bound the window. If a cache extension is installed, repeat calls fetch only the days newer than what is already stored; without one, every call fetches the full window from Substack. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
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
        description="Fetch the publication's trailing-30-day view count and its delta versus the prior period. Without a cache extension installed, every call reaches the Substack API directly. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
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
        description="Fetch the publication's daily annualized recurring revenue (ARR) timeseries for the trailing 7 days by default; each point keeps the raw money string next to the parsed number. Optionally pass `from_date` (ISO) to bound the window. If a cache extension is installed, repeat calls fetch only the days newer than what is already stored; without one, every call fetches the full window from Substack. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"stats", "read"},
        annotations=ToolAnnotations(
            title="Get ARR Timeseries",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "stats",
            "substack_endpoint": "GET /publication/stats/arr/timeseries",
        },
    )(get_arr_timeseries)
    mcp.tool(
        description="Fetch the publication's daily email subscriber count timeseries for the trailing 7 days by default. Optionally pass `from_date` (ISO) to bound the window. If a cache extension is installed, repeat calls fetch only the days newer than what is already stored; without one, every call fetches the full window from Substack. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"stats", "read"},
        annotations=ToolAnnotations(
            title="Get Email Timeseries",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "stats",
            "substack_endpoint": "GET /publication/stats/emails/timeseries",
        },
    )(get_email_timeseries)
    mcp.tool(
        description="Fetch the publish dashboard's headline numbers for the publication (views, subscribers and related totals). Without a cache extension installed, every call reaches the Substack API directly. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"stats", "read"},
        annotations=ToolAnnotations(
            title="Get Dashboard Summary",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "stats",
            "substack_endpoint": "GET /publish-dashboard/summary",
        },
    )(get_dashboard_summary)
    mcp.tool(
        description="Fetch the publish dashboard summary over a trailing window: pass `range_days` (1-3650, default 365) to choose the number of days. Without a cache extension installed, every call reaches the Substack API directly. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"stats", "read"},
        annotations=ToolAnnotations(
            title="Get Dashboard Period",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "stats",
            "substack_endpoint": "GET /publish-dashboard/summary-v2",
        },
    )(get_dashboard_period)
    mcp.tool(
        description="Fetch recommendation stats for the publication: pass `direction` `outgoing` (publications this one recommends) or `incoming` (publications recommending this one), paginated via `offset` (default 0) and `limit` (1-100, default 20). Without a cache extension installed, every call reaches the Substack API directly. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"stats", "read"},
        annotations=ToolAnnotations(
            title="Get Recommendation Stats",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "stats",
            "substack_endpoint": "GET /recommendations/stats/{from|to}",
        },
    )(get_recommendation_stats)
    mcp.tool(
        description="Fetch the publication's post counts by state (published, drafts, scheduled and so on). Without a cache extension installed, every call reaches the Substack API directly. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
        tags={"stats", "read"},
        annotations=ToolAnnotations(
            title="Get Post Counts",
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        meta={
            "category": "stats",
            "substack_endpoint": "GET /post_management/counts",
        },
    )(get_post_counts)
    mcp.tool(
        description="Fetch engagement for a published post: like count and likers, comment count and summary, and commenter count. Without a cache extension installed, every call reaches the Substack API directly. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
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
        description="Fetch traffic for a published post: view counts broken down by referrer source, device type, and category. Without a cache extension installed, every call reaches the Substack API directly. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
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
        description="Fetch per-recipient email stats for a published post (delivery, opens, clicks), paginated via limit/offset. Without a cache extension installed, every call reaches the Substack API directly. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
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
        description="Fetch subscriber growth attributed to a published post. Without a cache extension installed, every call reaches the Substack API directly. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
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
        description="Fetch the discussion (comment thread) for a published post, cursor-paginated. Without a cache extension installed, every call reaches the Substack API directly. The `token` argument is optional: pass base64-encoded Substack credentials, or omit it if this deployment resolves credentials from the authenticated session.",
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
