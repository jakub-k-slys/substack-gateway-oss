from __future__ import annotations

import pytest

from gateway_stats.schemas import (
    ArrPoint,
    ArrTimeseriesResponse,
    EmailTimeseriesResponse,
    parse_money,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("$258.19", 258.19),
        ("$1,262.40", 1262.40),
        ("-$5.00", -5.0),
        ("€12", 12.0),
        (" $ 7 ", 7.0),
        (12, 12.0),
        (12.5, 12.5),
        (None, None),
        (True, None),
        ("", None),
        ("n/a", None),
        ("€1.234,56", None),
        ("1,5", None),
        ("$1,23", None),
    ],
)
def test_parse_money(raw: object, expected: float | None) -> None:
    assert parse_money(raw) == expected


def test_arr_timeseries_from_substack() -> None:
    resp = ArrTimeseriesResponse.from_substack(
        [["2025/10/18", "$258.19"], ["2025/10/19", None]]
    )
    assert resp.items[0].model_dump() == {
        "date": "2025/10/18",
        "arr": 258.19,
        "arr_display": "$258.19",
    }
    assert resp.items[1].model_dump() == {
        "date": "2025/10/19",
        "arr": None,
        "arr_display": None,
    }


def test_arr_point_numeric_cell_keeps_display_as_string() -> None:
    assert ArrPoint.from_row(["2025/10/18", 258.19]).arr_display == "258.19"


def test_email_timeseries_from_substack_short_row() -> None:
    resp = EmailTimeseriesResponse.from_substack([["2025/10/19", 411], ["2025/10/20"]])
    assert [p.model_dump() for p in resp.items] == [
        {"date": "2025/10/19", "emails": 411},
        {"date": "2025/10/20", "emails": None},
    ]


def test_empty_timeseries_responses() -> None:
    assert ArrTimeseriesResponse.from_substack([]).items == []
    assert EmailTimeseriesResponse.from_substack([]).items == []
