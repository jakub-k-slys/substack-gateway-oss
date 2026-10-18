from __future__ import annotations

import math
import re
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


_MONEY_PLAIN = re.compile(r"\d+(\.\d+)?")
_MONEY_GROUPED = re.compile(r"\d{1,3}(,\d{3})+(\.\d+)?")
# [-] [symbol of 0-3 chars] [-] number, with optional whitespace between parts.
_MONEY_SHAPE = re.compile(r"\s*(-?)\s*[^\d\s.,\-]{0,3}\s*(-?)\s*([\d.,]+)\s*")


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
    """One day on the annualized-recurring-revenue timeseries.

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
    """One day on the emails-sent timeseries: ``[Date, Emails]``."""

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
