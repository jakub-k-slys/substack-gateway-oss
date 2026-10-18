from __future__ import annotations

import pytest

from gateway_stats.schemas import (
    ArrPoint,
    ArrTimeseriesResponse,
    DashboardPeriodResponse,
    DashboardSummaryResponse,
    EmailTimeseriesResponse,
    PeriodValue,
    PostCountsResponse,
    RecommendationStat,
    RecommendationStatsResponse,
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
        ("$1.2K", None),
        ("1.5M", None),
        ("1e5", None),
        ("Q3 2025", None),
        ("5-3", None),
        ("2025-10", None),
        ("12 USD", None),
        ("US$12", 12.0),
        ("-$1,262.40", -1262.40),
        ("$-5", -5.0),
        ("\u22125", -5.0),
        ("\u2212$5.00", -5.0),
        ("$\u22125", -5.0),
        (float("nan"), None),
        (float("inf"), None),
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


def test_arr_point_short_row() -> None:
    point = ArrPoint.from_row(["2025/10/18"])
    assert point.arr is None
    assert point.arr_display is None


def test_email_timeseries_from_substack_short_row() -> None:
    resp = EmailTimeseriesResponse.from_substack([["2025/10/19", 411], ["2025/10/20"]])
    assert [p.model_dump() for p in resp.items] == [
        {"date": "2025/10/19", "emails": 411},
        {"date": "2025/10/20", "emails": None},
    ]


def test_empty_timeseries_responses() -> None:
    assert ArrTimeseriesResponse.from_substack([]).items == []
    assert EmailTimeseriesResponse.from_substack([]).items == []


def test_dashboard_summary_maps_all_fields() -> None:
    resp = DashboardSummaryResponse.from_substack(
        {
            "appSubscribers": 12,
            "appSubscribersLast30Days": 3,
            "subscribers": 420,
            "subscribersLast30Days": 25,
            "totalEmail": 410,
            "totalEmailLast30Days": 22,
            "arr": "$1,262.40",
            "arrDelta": 54.1,
            "views": 9000,
            "viewsDelta": -120,
            "openRate": 0.48,
            "openRateDiff": -0.02,
            "pledgesAmount": "$30.00",
            "numPledges": 4,
            "pledgeCurrency": "usd",
            "isBestseller": False,
        }
    )
    assert resp.app_subscribers == 12
    assert resp.app_subscribers_last_30_days == 3
    assert resp.subscribers == 420
    assert resp.subscribers_last_30_days == 25
    assert resp.total_email == 410
    assert resp.total_email_last_30_days == 22
    assert resp.arr == 1262.40
    assert resp.arr_delta == 54.1
    assert resp.views == 9000
    assert resp.views_delta == -120
    assert resp.open_rate == 0.48
    assert resp.open_rate_diff == -0.02
    assert resp.pledges_amount == 30.0
    assert resp.num_pledges == 4
    assert resp.pledge_currency == "usd"
    assert resp.is_bestseller is False


def test_dashboard_summary_all_null() -> None:
    keys = (
        "appSubscribers",
        "appSubscribersLast30Days",
        "subscribers",
        "subscribersLast30Days",
        "totalEmail",
        "totalEmailLast30Days",
        "arr",
        "arrDelta",
        "views",
        "viewsDelta",
        "openRate",
        "openRateDiff",
        "pledgesAmount",
        "numPledges",
        "pledgeCurrency",
        "isBestseller",
    )
    for payload in ({}, dict.fromkeys(keys)):
        dumped = DashboardSummaryResponse.from_substack(payload).model_dump()
        assert len(dumped) == len(keys)
        assert all(v is None for v in dumped.values())


def test_dashboard_period_groups_start_end() -> None:
    resp = DashboardPeriodResponse.from_substack(
        {
            "totalSubscribersStart": 300,
            "totalSubscribersEnd": 420,
            "paidSubscribersStart": 20,
            "paidSubscribersEnd": 31,
            "arrStart": "$900.00",
            "arrEnd": "$1,262.40",
            "totalViewsStart": 5000,
            "totalViewsEnd": 9000,
            "pledgedArrStart": None,
            "pledgedArrEnd": "$360.00",
        },
        365,
    )
    assert resp.range_days == 365
    assert resp.total_subscribers == PeriodValue(start=300, end=420)
    assert isinstance(resp.total_subscribers.end, int)
    assert resp.paid_subscribers == PeriodValue(start=20, end=31)
    assert resp.arr.start == 900.0
    assert resp.arr.end == 1262.4
    assert resp.total_views == PeriodValue(start=5000, end=9000)
    assert resp.pledged_arr == PeriodValue(start=None, end=360.0)


def test_dashboard_period_partial_payload() -> None:
    resp = DashboardPeriodResponse.from_substack({}, 30)
    assert resp.range_days == 30
    assert resp.arr == PeriodValue(start=None, end=None)
    assert resp.total_subscribers == PeriodValue(start=None, end=None)


def test_recommendation_stat_from_slim_row() -> None:
    stat = RecommendationStat.from_substack(
        {
            "publication_id": 11,
            "target_publication_id": 22,
            "xp_signups": 40,
            "xp_signups_last_30_days": 5,
            "xp_paid_subs": 2,
            "is_mutual": True,
            "is_active": False,
            "created_at": "2025-01-02T03:04:05Z",
            "first_activity_at": "2025-01-03T00:00:00Z",
            "data_updated_at": "2025-10-18T00:00:00Z",
            "pub": {
                "id": 22,
                "name": "Fictional Weekly",
                "subdomain": "fictional",
                "custom_domain": None,
                "logo_url": "https://example.test/logo.png",
            },
        },
        "outgoing",
    )
    assert stat.model_dump() == {
        "publication": {
            "id": 22,
            "name": "Fictional Weekly",
            "subdomain": "fictional",
            "custom_domain": None,
            "logo_url": "https://example.test/logo.png",
        },
        "signups": 40,
        "signups_last_30_days": 5,
        "paid_subs": 2,
        "is_mutual": True,
        "is_active": False,
        "created_at": "2025-01-02T03:04:05Z",
        "first_activity_at": "2025-01-03T00:00:00Z",
        "data_updated_at": "2025-10-18T00:00:00Z",
    }


def test_recommendation_stat_from_raw_source_pub() -> None:
    stat = RecommendationStat.from_substack(
        {
            "publication_id": 33,
            "xp_signups": 7,
            "source_pub": {
                "id": 33,
                "name": "Invented Digest",
                "subdomain": "invented",
            },
            "extra_field": "ignored",
        },
        "incoming",
    )
    assert stat.publication.id == 33
    assert stat.publication.name == "Invented Digest"
    assert stat.publication.subdomain == "invented"
    assert stat.publication.logo_url is None
    assert stat.signups == 7
    assert stat.signups_last_30_days is None
    assert stat.is_mutual is None


def test_recommendation_stat_raw_target_pub() -> None:
    stat = RecommendationStat.from_substack(
        {"target_pub": {"id": 5, "name": "Made Up Notes"}}, "outgoing"
    )
    assert stat.publication.id == 5
    assert stat.publication.name == "Made Up Notes"


@pytest.mark.parametrize(
    ("direction", "row"),
    [
        ("outgoing", {"target_pub": {"id": 2002}, "source_pub": {"id": 1}}),
        ("incoming", {"target_pub": {"id": 1}, "source_pub": {"id": 2002}}),
    ],
)
def test_recommendation_stat_raw_row_with_both_pubs_picks_counterpart(
    direction: str, row: dict
) -> None:
    stat = RecommendationStat.from_substack(row, direction)
    assert stat.publication.id == 2002


def test_recommendation_stat_pub_key_wins_over_raw_keys() -> None:
    stat = RecommendationStat.from_substack(
        {
            "pub": {"id": 7},
            "target_pub": {"id": 1},
            "source_pub": {"id": 2},
        },
        "incoming",
    )
    assert stat.publication.id == 7


def test_recommendation_stat_null_pub_falls_back_to_row_id() -> None:
    row = {"publication_id": 11, "target_publication_id": 22, "pub": None}
    outgoing = RecommendationStat.from_substack(row, "outgoing")
    incoming = RecommendationStat.from_substack(row, "incoming")
    assert outgoing.publication.id == 22
    assert outgoing.publication.name is None
    assert incoming.publication.id == 11


def test_recommendation_stat_pub_without_id_falls_back_to_row_id() -> None:
    stat = RecommendationStat.from_substack(
        {"target_publication_id": 22, "pub": {"name": "Fictional Weekly"}},
        "outgoing",
    )
    assert stat.publication.id == 22
    assert stat.publication.name == "Fictional Weekly"


def test_recommendation_stats_next_offset() -> None:
    rows = [{"target_publication_id": 1}, {"target_publication_id": 2}]
    full = RecommendationStatsResponse.from_substack(
        {"rows": rows}, "outgoing", offset=0, limit=2
    )
    assert full.direction == "outgoing"
    assert [i.publication.id for i in full.items] == [1, 2]
    assert full.next_offset == 2

    paged = RecommendationStatsResponse.from_substack(
        {"rows": rows}, "incoming", offset=40, limit=2
    )
    assert paged.next_offset == 42

    short = RecommendationStatsResponse.from_substack(
        {"rows": rows[:1]}, "outgoing", offset=0, limit=2
    )
    assert short.next_offset is None

    empty = RecommendationStatsResponse.from_substack(
        {"rows": None}, "outgoing", offset=0, limit=2
    )
    assert empty.items == []
    assert empty.next_offset is None
    assert (
        RecommendationStatsResponse.from_substack(
            {}, "incoming", offset=0, limit=2
        ).items
        == []
    )


def test_post_counts_maps_flags() -> None:
    resp = PostCountsResponse.from_substack(
        {
            "published": 120,
            "publishedIsCapped": False,
            "drafts": 7,
            "draftsIsCapped": True,
            "scheduled": 2,
            "scheduledIsCapped": False,
        }
    )
    assert resp.model_dump() == {
        "published": 120,
        "published_is_capped": False,
        "drafts": 7,
        "drafts_is_capped": True,
        "scheduled": 2,
        "scheduled_is_capped": False,
    }


def test_post_counts_partial_payload() -> None:
    assert all(
        v is None for v in PostCountsResponse.from_substack({}).model_dump().values()
    )
