from __future__ import annotations

import math
import re
from typing import Any, Literal

from pydantic import BaseModel, Field, RootModel


class SubscriberPoint(BaseModel):
    """One day on the subscriber timeseries.

    Substack returns rows positionally as
    ``[Date, Paid, Comps, Free trials, Total subscribers]``.
    """

    date: str
    paid: int | None = None
    comps: int | None = None
    free_trials: int | None = None
    total: int | None = None

    @classmethod
    def from_row(cls, row: list) -> SubscriberPoint:
        cells = list(row) + [None] * (5 - len(row))
        return cls(
            date=cells[0],
            paid=cells[1],
            comps=cells[2],
            free_trials=cells[3],
            total=cells[4],
        )


class SubscriberTimeseriesResponse(BaseModel):
    items: list[SubscriberPoint]

    @classmethod
    def from_substack(cls, rows: list[list]) -> SubscriberTimeseriesResponse:
        return cls(items=[SubscriberPoint.from_row(r) for r in rows])


_MONEY_PLAIN = re.compile(r"\d+(\.\d+)?")
_MONEY_GROUPED = re.compile(r"\d{1,3}(,\d{3})+(\.\d+)?")
# [-] [symbol of 0-3 chars] [-] number, with optional whitespace between parts.
# The Unicode minus (U+2212) counts as "-" in both sign positions.
_MONEY_SHAPE = re.compile(
    r"\s*([-\u2212]?)\s*[^\d\s.,\-\u2212]{0,3}\s*([-\u2212]?)\s*([\d.,]+)\s*"
)


def parse_money(value: object) -> float | None:
    """Parse a Substack money cell (``"$1,262.40"``) into a float.

    Currency symbols are discarded, never interpreted. Ambiguous or
    locale-formatted or otherwise unrecognised strings (``"€1.234,56"``,
    ``"1.5M"``, ``"12 USD"``) yield ``None`` rather than a guessed number.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value) if math.isfinite(value) else None
    if not isinstance(value, str):
        return None
    shape = _MONEY_SHAPE.fullmatch(value)
    if shape is None:
        return None
    negative = bool(shape.group(1) or shape.group(2))
    digits = shape.group(3)
    if _MONEY_PLAIN.fullmatch(digits):
        number = float(digits)
    elif _MONEY_GROUPED.fullmatch(digits):
        number = float(digits.replace(",", ""))
    else:
        return None
    return -number if negative else number


class ArrPoint(BaseModel):
    """One day on the annualized recurring revenue timeseries.

    Substack returns rows positionally as ``[Date, ARR]`` where ARR is a
    formatted money string. The raw string is kept next to the parsed number.
    """

    date: str
    arr: float | None = None
    arr_display: str | None = None

    @classmethod
    def from_row(cls, row: list) -> ArrPoint:
        cells = list(row) + [None] * (2 - len(row))
        cell = cells[1]
        return cls(
            date=cells[0],
            arr=parse_money(cell),
            arr_display=None if cell is None else str(cell),
        )


class ArrTimeseriesResponse(BaseModel):
    items: list[ArrPoint]

    @classmethod
    def from_substack(cls, rows: list[list]) -> ArrTimeseriesResponse:
        return cls(items=[ArrPoint.from_row(r) for r in rows])


class EmailPoint(BaseModel):
    """One day on the email-subscriber count timeseries: ``[Date, Emails]``."""

    date: str
    emails: int | None = None

    @classmethod
    def from_row(cls, row: list) -> EmailPoint:
        cells = list(row) + [None] * (2 - len(row))
        return cls(date=cells[0], emails=cells[1])


class EmailTimeseriesResponse(BaseModel):
    items: list[EmailPoint]

    @classmethod
    def from_substack(cls, rows: list[list]) -> EmailTimeseriesResponse:
        return cls(items=[EmailPoint.from_row(r) for r in rows])


class ThirtyDayViewsResponse(BaseModel):
    views_30d: int = 0
    views_delta_30d: int = 0

    @classmethod
    def from_substack(cls, data: dict) -> ThirtyDayViewsResponse:
        return cls(
            views_30d=data.get("views30d", 0) or 0,
            views_delta_30d=data.get("viewsDelta30d", 0) or 0,
        )


# --- Per-post stats --------------------------------------------------------
#
# These tabs are large, nested Substack objects. We pin the meaningful
# top-level structure and pass the deeply-nested rows through untyped so the
# gateway stays faithful to (and resilient against changes in) Substack's shape.


class PostEngagementResponse(BaseModel):
    likes_count: int = 0
    comment_count: int = 0
    commenter_count: int = 0
    likes: list[dict[str, Any]] = Field(default_factory=list)
    comments: list[dict[str, Any]] = Field(default_factory=list)
    commenters: list[dict[str, Any]] = Field(default_factory=list)

    @classmethod
    def from_substack(cls, data: dict) -> PostEngagementResponse:
        likes = data.get("likes") or {}
        summary = data.get("commentSummary") or {}
        commenters = data.get("commenters") or {}
        return cls(
            likes_count=likes.get("count", 0) or 0,
            comment_count=summary.get("total", 0) or 0,
            commenter_count=commenters.get("count", 0) or 0,
            likes=likes.get("users") or [],
            comments=summary.get("comments") or [],
            commenters=commenters.get("users") or [],
        )


class PostTrafficResponse(BaseModel):
    referrers: list[dict[str, Any]] = Field(default_factory=list)
    devices: list[dict[str, Any]] = Field(default_factory=list)
    categories: list[dict[str, Any]] = Field(default_factory=list)

    @classmethod
    def from_substack(cls, data: dict) -> PostTrafficResponse:
        return cls(
            referrers=data.get("referrers") or [],
            devices=data.get("devices") or [],
            categories=data.get("categories") or [],
        )


class PostRecipientsResponse(BaseModel):
    rows: list[dict[str, Any]] = Field(default_factory=list)
    total: int = 0

    @classmethod
    def from_substack(cls, data: dict) -> PostRecipientsResponse:
        return cls(rows=data.get("rows") or [], total=data.get("total", 0) or 0)


class PostDiscussionResponse(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)
    next_cursor: str | None = None
    tabs: list[dict[str, Any]] = Field(default_factory=list)
    tab_id: str | None = None

    @classmethod
    def from_substack(cls, data: dict) -> PostDiscussionResponse:
        return cls(
            items=data.get("items") or [],
            next_cursor=data.get("nextCursor"),
            tabs=data.get("tabs") or [],
            tab_id=data.get("tabId"),
        )


class PostGrowthResponse(RootModel[dict[str, Any]]):
    """Growth attribution — passed through verbatim (shape not yet pinned)."""

    @classmethod
    def from_substack(cls, data: dict) -> PostGrowthResponse:
        return cls(data)


# --- Dashboard -------------------------------------------------------------
#
# Aggregate snapshots of the publication dashboard. Substack sends camelCase
# keys (and money as formatted strings); these models expose snake_case and
# parsed numbers. Missing upstream keys map to ``None``, nothing raises on a
# partial payload.


class DashboardSummaryResponse(BaseModel):
    app_subscribers: int | None = None
    app_subscribers_last_30_days: int | None = None
    subscribers: int | None = None
    subscribers_last_30_days: int | None = None
    total_email: int | None = None
    total_email_last_30_days: int | None = None
    arr: float | None = None
    arr_delta: float | None = None
    views: int | None = None
    views_delta: int | None = None
    open_rate: float | None = None
    open_rate_diff: float | None = None
    pledges_amount: float | None = None
    num_pledges: int | None = None
    pledge_currency: str | None = None
    is_bestseller: bool | None = None

    @classmethod
    def from_substack(cls, data: dict) -> DashboardSummaryResponse:
        return cls(
            app_subscribers=data.get("appSubscribers"),
            app_subscribers_last_30_days=data.get("appSubscribersLast30Days"),
            subscribers=data.get("subscribers"),
            subscribers_last_30_days=data.get("subscribersLast30Days"),
            total_email=data.get("totalEmail"),
            total_email_last_30_days=data.get("totalEmailLast30Days"),
            arr=parse_money(data.get("arr")),
            arr_delta=parse_money(data.get("arrDelta")),
            views=data.get("views"),
            views_delta=data.get("viewsDelta"),
            open_rate=data.get("openRate"),
            open_rate_diff=data.get("openRateDiff"),
            pledges_amount=parse_money(data.get("pledgesAmount")),
            num_pledges=data.get("numPledges"),
            pledge_currency=data.get("pledgeCurrency"),
            is_bestseller=data.get("isBestseller"),
        )


class PeriodValue(BaseModel):
    """A metric at the start and end of a period."""

    start: int | float | None = None
    end: int | float | None = None


class DashboardPeriodResponse(BaseModel):
    range_days: int
    total_subscribers: PeriodValue
    paid_subscribers: PeriodValue
    arr: PeriodValue
    total_views: PeriodValue
    pledged_arr: PeriodValue

    @classmethod
    def from_substack(cls, data: dict, range_days: int) -> DashboardPeriodResponse:
        def count(key: str) -> PeriodValue:
            return PeriodValue(start=data.get(f"{key}Start"), end=data.get(f"{key}End"))

        def money(key: str) -> PeriodValue:
            return PeriodValue(
                start=parse_money(data.get(f"{key}Start")),
                end=parse_money(data.get(f"{key}End")),
            )

        return cls(
            range_days=range_days,
            total_subscribers=count("totalSubscribers"),
            paid_subscribers=count("paidSubscribers"),
            arr=money("arr"),
            total_views=count("totalViews"),
            pledged_arr=money("pledgedArr"),
        )


class RecommendedPublication(BaseModel):
    id: int | None = None
    name: str | None = None
    subdomain: str | None = None
    custom_domain: str | None = None
    logo_url: str | None = None


class RecommendationStat(BaseModel):
    """One recommendation relationship with its signup numbers.

    Accepts both the slimmed row (publication under ``pub``) and the raw
    Substack row (``target_pub`` for outgoing, ``source_pub`` for incoming).
    """

    publication: RecommendedPublication
    signups: int | None = None
    signups_last_30_days: int | None = None
    paid_subs: int | None = None
    is_mutual: bool | None = None
    is_active: bool | None = None
    created_at: str | None = None
    first_activity_at: str | None = None
    data_updated_at: str | None = None

    @classmethod
    def from_substack(cls, row: dict, direction: str) -> RecommendationStat:
        # Counterpart first: target_pub when outgoing, source_pub when incoming.
        counterpart = (
            ("source_pub", "target_pub")
            if direction == "incoming"
            else ("target_pub", "source_pub")
        )
        pub: dict = {}
        for key in ("pub", *counterpart):
            if isinstance(row.get(key), dict):
                pub = row[key]
                break
        pub_id = pub.get("id")
        if pub_id is None:
            pub_id = row.get(
                "target_publication_id" if direction == "outgoing" else "publication_id"
            )
        return cls(
            publication=RecommendedPublication(
                id=pub_id,
                name=pub.get("name"),
                subdomain=pub.get("subdomain"),
                custom_domain=pub.get("custom_domain"),
                logo_url=pub.get("logo_url"),
            ),
            signups=row.get("xp_signups"),
            signups_last_30_days=row.get("xp_signups_last_30_days"),
            paid_subs=row.get("xp_paid_subs"),
            is_mutual=row.get("is_mutual"),
            is_active=row.get("is_active"),
            created_at=row.get("created_at"),
            first_activity_at=row.get("first_activity_at"),
            data_updated_at=row.get("data_updated_at"),
        )


class RecommendationStatsResponse(BaseModel):
    direction: Literal["outgoing", "incoming"]
    items: list[RecommendationStat]
    next_offset: int | None = None

    @classmethod
    def from_substack(
        cls, data: dict, direction: str, offset: int, limit: int
    ) -> RecommendationStatsResponse:
        items = [
            RecommendationStat.from_substack(row, direction)
            for row in data.get("rows") or []
        ]
        return cls.model_validate(
            {
                "direction": direction,
                "items": items,
                "next_offset": offset + limit if len(items) == limit else None,
            }
        )


class PostCountsResponse(BaseModel):
    published: int | None = None
    published_is_capped: bool | None = None
    drafts: int | None = None
    drafts_is_capped: bool | None = None
    scheduled: int | None = None
    scheduled_is_capped: bool | None = None

    @classmethod
    def from_substack(cls, data: dict) -> PostCountsResponse:
        return cls(
            published=data.get("published"),
            published_is_capped=data.get("publishedIsCapped"),
            drafts=data.get("drafts"),
            drafts_is_capped=data.get("draftsIsCapped"),
            scheduled=data.get("scheduled"),
            scheduled_is_capped=data.get("scheduledIsCapped"),
        )
