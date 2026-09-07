from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from gateway_rest_common.deps import get_credentials
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
from gateway_stats_rest.deps import get_post_stats_service, get_stats_service

router = APIRouter()

_PostId = Annotated[int, Path(gt=0, description="Published post id.")]
_PostStatsService = Annotated[PostStatsService, Depends(get_post_stats_service)]


@router.get(
    "/stats/subscribers",
    response_model=SubscriberTimeseriesResponse,
    dependencies=[Depends(get_credentials)],
    tags=["stats"],
)
async def subscriber_timeseries(
    service: Annotated[StatsService, Depends(get_stats_service)],
    from_: Annotated[
        str | None,
        Query(
            alias="from",
            description="ISO lower bound for the returned window "
            "(e.g. 2025-07-09T00:00:00Z). Defaults to the last 365 days.",
        ),
    ] = None,
) -> SubscriberTimeseriesResponse:
    """Daily subscriber counts (paid / comps / free trials / total).

    Cached with delta fetch: only the tail beyond the last cached day is pulled
    from Substack on subsequent calls.
    """
    rows = await service.subscriber_timeseries(from_=from_)
    return SubscriberTimeseriesResponse.from_substack(rows)


@router.get(
    "/stats/30d-views",
    response_model=ThirtyDayViewsResponse,
    dependencies=[Depends(get_credentials)],
    tags=["stats"],
)
async def thirty_day_views(
    service: Annotated[StatsService, Depends(get_stats_service)],
) -> ThirtyDayViewsResponse:
    """Trailing-30-day publication views and their delta (TTL-cached snapshot)."""
    data = await service.thirty_day_views()
    return ThirtyDayViewsResponse.from_substack(data)


@router.get(
    "/posts/{post_id}/stats/engagement",
    response_model=PostEngagementResponse,
    dependencies=[Depends(get_credentials)],
    tags=["post-stats"],
)
async def post_engagement(
    post_id: _PostId, service: _PostStatsService
) -> PostEngagementResponse:
    """Likes, comment summary, and commenters for a post (TTL-cached)."""
    data = await service.engagement(post_id)
    return PostEngagementResponse.from_substack(data)


@router.get(
    "/posts/{post_id}/stats/traffic",
    response_model=PostTrafficResponse,
    dependencies=[Depends(get_credentials)],
    tags=["post-stats"],
)
async def post_traffic(
    post_id: _PostId, service: _PostStatsService
) -> PostTrafficResponse:
    """Referrers, devices, and category breakdown of a post's views."""
    data = await service.traffic(post_id)
    return PostTrafficResponse.from_substack(data)


@router.get(
    "/posts/{post_id}/stats/recipients",
    response_model=PostRecipientsResponse,
    dependencies=[Depends(get_credentials)],
    tags=["post-stats"],
)
async def post_recipients(
    post_id: _PostId,
    service: _PostStatsService,
    limit: Annotated[int, Query(gt=0, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> PostRecipientsResponse:
    """Per-recipient email delivery / open / click rows (paginated)."""
    data = await service.recipients(post_id, limit=limit, offset=offset)
    return PostRecipientsResponse.from_substack(data)


@router.get(
    "/posts/{post_id}/stats/growth",
    response_model=PostGrowthResponse,
    dependencies=[Depends(get_credentials)],
    tags=["post-stats"],
)
async def post_growth(
    post_id: _PostId, service: _PostStatsService
) -> PostGrowthResponse:
    """Subscriber growth attributed to a post."""
    data = await service.growth(post_id)
    return PostGrowthResponse.from_substack(data)


@router.get(
    "/posts/{post_id}/stats/discussion",
    response_model=PostDiscussionResponse,
    dependencies=[Depends(get_credentials)],
    tags=["post-stats"],
)
async def post_discussion(
    post_id: _PostId,
    service: _PostStatsService,
    cursor: Annotated[
        str | None, Query(description="Opaque discussion cursor.")
    ] = None,
) -> PostDiscussionResponse:
    """Comment / discussion thread for a post (cursor-paginated)."""
    data = await service.discussion(post_id, cursor=cursor)
    return PostDiscussionResponse.from_substack(data)
