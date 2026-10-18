from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field

from gateway_core.auth import BearerCredentials
from gateway_mcp_common.clients import clients_from, resolve_credentials
from gateway_stats.cache import get_stats_cache
from gateway_stats.dashboard import DashboardService
from gateway_stats.post_stats import PostStatsService
from gateway_stats.schemas import (
    ArrTimeseriesResponse,
    DashboardPeriodResponse,
    DashboardSummaryResponse,
    EmailTimeseriesResponse,
    PostCountsResponse,
    PostDiscussionResponse,
    PostEngagementResponse,
    PostGrowthResponse,
    PostRecipientsResponse,
    PostTrafficResponse,
    RecommendationStatsResponse,
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
            publication, substack, get_stats_cache(), credentials.publication_url
        ).subscriber_timeseries(from_=from_date)
    return SubscriberTimeseriesResponse.from_substack(rows).model_dump()


async def get_30d_views(
    token: str | None = None,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    assert credentials.publication_url is not None
    async with clients_from(credentials) as (publication, substack):
        data = await StatsService(
            publication, substack, get_stats_cache(), credentials.publication_url
        ).thirty_day_views()
    return ThirtyDayViewsResponse.from_substack(data).model_dump()


async def get_arr_timeseries(
    token: str | None = None,
    from_date: str | None = None,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    assert credentials.publication_url is not None
    async with clients_from(credentials) as (publication, substack):
        rows = await StatsService(
            publication, substack, get_stats_cache(), credentials.publication_url
        ).arr_timeseries(from_=from_date)
    return ArrTimeseriesResponse.from_substack(rows).model_dump()


async def get_email_timeseries(
    token: str | None = None,
    from_date: str | None = None,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    assert credentials.publication_url is not None
    async with clients_from(credentials) as (publication, substack):
        rows = await StatsService(
            publication, substack, get_stats_cache(), credentials.publication_url
        ).email_timeseries(from_=from_date)
    return EmailTimeseriesResponse.from_substack(rows).model_dump()


def _dashboard_service(
    credentials: BearerCredentials, publication, substack
) -> DashboardService:
    assert credentials.publication_url is not None
    return DashboardService(
        publication, substack, get_stats_cache(), credentials.publication_url
    )


async def get_dashboard_summary(
    token: str | None = None,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    async with clients_from(credentials) as (publication, substack):
        data = await _dashboard_service(credentials, publication, substack).summary()
    return DashboardSummaryResponse.from_substack(data).model_dump()


async def get_dashboard_period(
    token: str | None = None,
    range_days: Annotated[int, Field(ge=1, le=3650)] = 365,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    async with clients_from(credentials) as (publication, substack):
        data = await _dashboard_service(credentials, publication, substack).period(
            range_days
        )
    return DashboardPeriodResponse.from_substack(data, range_days).model_dump()


async def get_recommendation_stats(
    direction: Literal["outgoing", "incoming"],
    token: str | None = None,
    offset: Annotated[int, Field(ge=0)] = 0,
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    async with clients_from(credentials) as (publication, substack):
        data = await _dashboard_service(
            credentials, publication, substack
        ).recommendations(direction, offset=offset, limit=limit)
    return RecommendationStatsResponse.from_substack(
        data, direction, offset, limit
    ).model_dump()


async def get_post_counts(
    token: str | None = None,
) -> dict[str, Any]:
    credentials = await resolve_credentials(token)
    async with clients_from(credentials) as (publication, substack):
        data = await _dashboard_service(
            credentials, publication, substack
        ).post_counts()
    return PostCountsResponse.from_substack(data).model_dump()


def _post_stats_service(
    credentials: BearerCredentials, publication, substack
) -> PostStatsService:
    assert credentials.publication_url is not None
    return PostStatsService(
        publication, substack, get_stats_cache(), credentials.publication_url
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
