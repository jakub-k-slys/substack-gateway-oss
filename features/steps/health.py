from __future__ import annotations

import httpx
from behave import given
from packages.gateway_oss.features.steps.common import SUBSTACK_BASE

_FEED_FOLLOWING_URL = f"{SUBSTACK_BASE}/api/v1/feed/following"


@given("the Substack API is reachable")
def step_api_reachable(context):
    context.respx_mock.get(_FEED_FOLLOWING_URL).mock(return_value=httpx.Response(200))


@given("the Substack API is unreachable")
def step_api_unreachable(context):
    context.respx_mock.get(_FEED_FOLLOWING_URL).mock(
        side_effect=httpx.ConnectError("connection refused")
    )


@given("the Substack API times out")
def step_api_timeout(context):
    context.respx_mock.get(_FEED_FOLLOWING_URL).mock(
        side_effect=httpx.TimeoutException("request timed out")
    )


@given("the Substack feed/following endpoint returns status {status:d}")
def step_feed_following_returns_status(context, status):
    context.respx_mock.get(_FEED_FOLLOWING_URL).mock(
        return_value=httpx.Response(status)
    )
