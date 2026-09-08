from __future__ import annotations

from typing import Any

from gateway_core.auth import BearerCredentials
from gateway_mcp_common.clients import clients_from, resolve_credentials
from gateway_stats.cache import create_stats_cache
from gateway_stats.post_stats import PostStatsService
from gateway_stats.schemas import (
    PostDiscussionResponse,
    PostEngagementResponse,
    PostGrowthResponse,
    PostRecipientsResponse,
    PostTrafficResponse,
    SubscriberTimeseriesResponse,
    ThirtyDayViewsResponse,
)
from gateway_stats.service import StatsService


async def get_subscriber_timeseries(
    token: str | None = None,
    from_date: str | None = None,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    assert credentials.publication_url is not None
    async with clients_from(credentials) as (publication, substack):
        rows = await StatsService(
            publication, substack, create_stats_cache(), credentials.publication_url
        ).subscriber_timeseries(from_=from_date)
    return SubscriberTimeseriesResponse.from_substack(rows).model_dump()


async def get_30d_views(
    token: str | None = None,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    assert credentials.publication_url is not None
    async with clients_from(credentials) as (publication, substack):
        data = await StatsService(
            publication, substack, create_stats_cache(), credentials.publication_url
        ).thirty_day_views()
    return ThirtyDayViewsResponse.from_substack(data).model_dump()


def _post_stats_service(
    credentials: BearerCredentials, publication, substack
) -> PostStatsService:
    assert credentials.publication_url is not None
    return PostStatsService(
        publication, substack, create_stats_cache(), credentials.publication_url
    )


async def get_post_engagement(post_id: int, token: str | None = None) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    async with clients_from(credentials) as (publication, substack):
        data = await _post_stats_service(credentials, publication, substack).engagement(
            post_id
        )
    return PostEngagementResponse.from_substack(data).model_dump()


async def get_post_traffic(post_id: int, token: str | None = None) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    async with clients_from(credentials) as (publication, substack):
        data = await _post_stats_service(credentials, publication, substack).traffic(
            post_id
        )
    return PostTrafficResponse.from_substack(data).model_dump()


async def get_post_recipients(
    post_id: int,
    token: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    async with clients_from(credentials) as (publication, substack):
        data = await _post_stats_service(credentials, publication, substack).recipients(
            post_id, limit=limit, offset=offset
        )
    return PostRecipientsResponse.from_substack(data).model_dump()


async def get_post_growth(post_id: int, token: str | None = None) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    async with clients_from(credentials) as (publication, substack):
        data = await _post_stats_service(credentials, publication, substack).growth(
            post_id
        )
    return PostGrowthResponse.from_substack(data).model_dump()


async def get_post_discussion(
    post_id: int,
    token: str | None = None,
    cursor: str | None = None,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    async with clients_from(credentials) as (publication, substack):
        data = await _post_stats_service(credentials, publication, substack).discussion(
            post_id, cursor=cursor
        )
    return PostDiscussionResponse.from_substack(data).model_dump()
