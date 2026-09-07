from __future__ import annotations

import httpx
from behave import given
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
