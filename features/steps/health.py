from __future__ import annotations

import httpx
from behave import given

_USER_SETTING_PATH = "/api/v1/user-setting"


def _user_setting_url(context) -> str:
    pub_url = context.headers.get("x-publication-url", "").rstrip("/")
    return f"{pub_url}{_USER_SETTING_PATH}"


@given("the Substack API is reachable")
def step_api_reachable(context):
    context.respx_mock.put(_user_setting_url(context)).mock(
        return_value=httpx.Response(200)
    )


@given("the Substack API is unreachable")
def step_api_unreachable(context):
    context.respx_mock.put(_user_setting_url(context)).mock(
        side_effect=httpx.ConnectError("connection refused")
    )
