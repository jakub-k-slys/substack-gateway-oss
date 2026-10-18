from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from gateway_rest_common.deps import get_credentials
from gateway_stats.dashboard import DashboardService, RecommendationDirection
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
from gateway_stats_rest.deps import (
    get_dashboard_service,
    get_post_stats_service,
    get_stats_service,
)

router = APIRouter()

_PostId = Annotated[int, Path(gt=0, description="Published post id.")]
_PostStatsService = Annotated[PostStatsService, Depends(get_post_stats_service)]
_DashboardService = Annotated[DashboardService, Depends(get_dashboard_service)]
_FromParam = Annotated[
    str | None,
    Query(
        alias="from",
        pattern=r"^\d{4}-\d{2}-\d{2}",
        description="ISO lower bound for the returned window "
        "(e.g. 2025-07-09T00:00:00Z). Defaults to the last 7 days.",
    ),
]


@router.get(
    "/stats/subscribers",
    response_model=SubscriberTimeseriesResponse,
    dependencies=[Depends(get_credentials)],
    tags=["stats"],
)
async def subscriber_timeseries(
    service: Annotated[StatsService, Depends(get_stats_service)],
    from_: _FromParam = None,
) -> SubscriberTimeseriesResponse:
    """Daily subscriber counts (paid / comps / free trials / total).

    If a cache extension is installed, only the tail beyond the last stored
    day is fetched from Substack on subsequent calls; without one, every call
    fetches the full window.
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
    """Trailing-30-day publication views and their delta.

    Without a cache extension installed, every call reaches the Substack API
    directly.
    """
    data = await service.thirty_day_views()
    return ThirtyDayViewsResponse.from_substack(data)


@router.get(
    "/stats/arr",
    response_model=ArrTimeseriesResponse,
    dependencies=[Depends(get_credentials)],
    tags=["stats"],
)
async def arr_timeseries(
    service: Annotated[StatsService, Depends(get_stats_service)],
    from_: _FromParam = None,
) -> ArrTimeseriesResponse:
    """Daily annualized recurring revenue (ARR) as a timeseries.

    Each point carries the parsed amount and the display string exactly as
    Substack sent it. If a cache extension is installed, only the tail beyond
    the last stored day is fetched from Substack on subsequent calls; without
    one, every call fetches the full window.
    """
    rows = await service.arr_timeseries(from_=from_)
    return ArrTimeseriesResponse.from_substack(rows)


@router.get(
    "/stats/emails",
    response_model=EmailTimeseriesResponse,
    dependencies=[Depends(get_credentials)],
    tags=["stats"],
)
async def email_timeseries(
    service: Annotated[StatsService, Depends(get_stats_service)],
    from_: _FromParam = None,
) -> EmailTimeseriesResponse:
    """Daily email subscriber counts as a timeseries.

    If a cache extension is installed, only the tail beyond the last stored
    day is fetched from Substack on subsequent calls; without one, every call
    fetches the full window.
    """
    rows = await service.email_timeseries(from_=from_)
    return EmailTimeseriesResponse.from_substack(rows)


@router.get(
    "/stats/dashboard",
    response_model=DashboardSummaryResponse,
    dependencies=[Depends(get_credentials)],
    tags=["stats"],
)
async def dashboard_summary(service: _DashboardService) -> DashboardSummaryResponse:
    """Headline dashboard numbers: subscribers, ARR, views, open rate, pledges.

    Without a cache extension installed, every call reaches the Substack API
    directly.
    """
    data = await service.summary()
    return DashboardSummaryResponse.from_substack(data)


@router.get(
    "/stats/dashboard/period",
    response_model=DashboardPeriodResponse,
    dependencies=[Depends(get_credentials)],
    tags=["stats"],
)
async def dashboard_period(
    service: _DashboardService,
    range_days: Annotated[
        int,
        Query(ge=1, le=3650, description="Trailing window length in days."),
    ] = 365,
) -> DashboardPeriodResponse:
    """Start and end values of the key dashboard metrics over a trailing window.

    Without a cache extension installed, every call reaches the Substack API
    directly.
    """
    data = await service.period(range_days)
    return DashboardPeriodResponse.from_substack(data, range_days)


@router.get(
    "/stats/recommendations/{direction}",
    response_model=RecommendationStatsResponse,
    dependencies=[Depends(get_credentials)],
    tags=["stats"],
)
async def recommendation_stats(
    direction: RecommendationDirection,
    service: _DashboardService,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> RecommendationStatsResponse:
    """Recommendation signup stats (paginated).

    `outgoing` lists publications this one recommends; `incoming` lists
    publications recommending this one. Without a cache extension installed,
    every call reaches the Substack API directly.
    """
    data = await service.recommendations(direction, offset=offset, limit=limit)
    return RecommendationStatsResponse.from_substack(data, direction, offset, limit)


@router.get(
    "/stats/posts/counts",
    response_model=PostCountsResponse,
    dependencies=[Depends(get_credentials)],
    tags=["stats"],
)
async def post_counts(service: _DashboardService) -> PostCountsResponse:
    """Post counts by state (published, drafts, scheduled).

    Without a cache extension installed, every call reaches the Substack API
    directly.
    """
    data = await service.post_counts()
    return PostCountsResponse.from_substack(data)


@router.get(
    "/posts/{post_id}/stats/engagement",
    response_model=PostEngagementResponse,
    dependencies=[Depends(get_credentials)],
    tags=["post-stats"],
)
async def post_engagement(
    post_id: _PostId, service: _PostStatsService
) -> PostEngagementResponse:
    """Likes, comment summary, and commenters for a post.

    Without a cache extension installed, every call reaches the Substack API
    directly.
    """
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
