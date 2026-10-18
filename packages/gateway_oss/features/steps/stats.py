from __future__ import annotations

import json

import httpx
from behave import given, then
from common import load_sample, pub_url


def _subscribers_url(context) -> str:
    return f"{pub_url(context)}/api/v1/publication/stats/subscribers/timeseries"


def _views_url(context) -> str:
    return f"{pub_url(context)}/api/v1/publication/stats/publication_traffic/30d_views"


@given("the Substack subscriber-timeseries endpoint returns the sample response")
def step_subscribers_sample(context):
    context.respx_mock.get(_subscribers_url(context)).mock(
        return_value=httpx.Response(
            200, json=load_sample("api/v1/stats/subscribers-timeseries")
        )
    )


@given("the Substack subscriber-timeseries endpoint returns status {status:d}")
def step_subscribers_status(context, status):
    context.respx_mock.get(_subscribers_url(context)).mock(
        return_value=httpx.Response(status)
    )


@given("the Substack 30d-views endpoint returns the sample response")
def step_views_sample(context):
    context.respx_mock.get(_views_url(context)).mock(
        return_value=httpx.Response(200, json=load_sample("api/v1/stats/30d-views"))
    )


@given("the Substack 30d-views endpoint returns status {status:d}")
def step_views_status(context, status):
    context.respx_mock.get(_views_url(context)).mock(
        return_value=httpx.Response(status)
    )


# name -> (upstream path under /api/v1/, sample file under samples/api/v1/stats/)
_STATS_ENDPOINTS = {
    "ARR-timeseries": ("publication/stats/arr/timeseries", "arr-timeseries"),
    "email-timeseries": ("publication/stats/emails/timeseries", "emails-timeseries"),
    "dashboard-summary": ("publish-dashboard/summary", "dashboard-summary"),
    "dashboard-period": ("publish-dashboard/summary-v2", "dashboard-summary-v2"),
    "recommendations-from": ("recommendations/stats/from", "recommendations-from"),
    "recommendations-to": ("recommendations/stats/to", "recommendations-to"),
    "post-counts": ("post_management/counts", "post-counts"),
}


def _stats_endpoint(context, name: str) -> tuple[str, str]:
    assert name in _STATS_ENDPOINTS, (
        f"Unknown stats endpoint {name!r}; expected one of {sorted(_STATS_ENDPOINTS)}"
    )
    path, sample = _STATS_ENDPOINTS[name]
    return f"{pub_url(context)}/api/v1/{path}", f"api/v1/stats/{sample}"


@given('the Substack stats "{name}" endpoint returns the sample response')
def step_stats_sample(context, name):
    url, sample = _stats_endpoint(context, name)
    context.respx_mock.get(url).mock(
        return_value=httpx.Response(200, json=load_sample(sample))
    )


@given('the Substack stats "{name}" endpoint returns status {status:d}')
def step_stats_status(context, name, status):
    url, _ = _stats_endpoint(context, name)
    context.respx_mock.get(url).mock(return_value=httpx.Response(status))


@then('the response path "{path}" equals JSON {value}')
def step_path_equals_json(context, path, value):
    node = context.response.json()
    for segment in path.split("."):
        node = node[int(segment)] if isinstance(node, list) else node[segment]
    expected = json.loads(value)
    assert node == expected, f"Expected {path} to equal {expected!r}, got {node!r}"
