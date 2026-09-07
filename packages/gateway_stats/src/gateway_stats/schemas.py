from __future__ import annotations

from typing import Any

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
