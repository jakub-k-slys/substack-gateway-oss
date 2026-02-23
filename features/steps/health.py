from __future__ import annotations

import httpx
from behave import given

from features.steps.common import user_setting_url


@given("the Substack API is reachable")
def step_api_reachable(context):
    context.respx_mock.put(user_setting_url()).mock(
        return_value=httpx.Response(200)
    )


@given("the Substack API is unreachable")
def step_api_unreachable(context):
    context.respx_mock.put(user_setting_url()).mock(
        side_effect=httpx.ConnectError("connection refused")
    )
