from __future__ import annotations

import httpx
from behave import given
from packages.gateway_oss.features.steps.common import (
    SUBSTACK_BASE,
    load_sample,
    public_profile_url,
    user_setting_url,
)

_HANDLE_OPTIONS_PATH = "/api/v1/handle/options"


def _handle_options_url() -> str:
    return f"{SUBSTACK_BASE}{_HANDLE_OPTIONS_PATH}"


def _notes_url(context) -> str:
    pub = context.headers.get("x-publication-url")
    if not pub:
        raise RuntimeError("x-publication-url not set — missing a Given step?")
    return f"{pub.rstrip('/')}/api/v1/notes"


def _profile_posts_url() -> str:
    return f"{SUBSTACK_BASE}/api/v1/profile/posts"


def _subscriber_lists_url(context, user_id: int) -> str:
    pub = context.headers.get("x-publication-url")
    if not pub:
        raise RuntimeError("x-publication-url not set — missing a Given step?")
    return f"{pub.rstrip('/')}/api/v1/user/{user_id}/subscriber-lists"


@given("the Substack handles endpoint returns the sample response")
def step_handles_returns_sample(context):
    context.respx_mock.get(_handle_options_url()).mock(
        return_value=httpx.Response(200, json=load_sample("api/v1/handle/options"))
    )


@given(
    'the Substack public profile endpoint returns the sample response for "{handle}"'
)
def step_public_profile_returns_sample(context, handle):
    context.respx_mock.get(public_profile_url(handle)).mock(
        return_value=httpx.Response(
            200, json=load_sample(f"api/v1/user/{handle}/public_profile")
        )
    )


@given("the Substack handles endpoint returns the empty handles response")
def step_handles_returns_empty(context):
    context.respx_mock.get(_handle_options_url()).mock(
        return_value=httpx.Response(200, json={"potentialHandles": []})
    )


@given("the Substack handles endpoint returns status {status:d}")
def step_handles_returns_status(context, status):
    context.respx_mock.get(_handle_options_url()).mock(
        return_value=httpx.Response(status)
    )


@given("the Substack notes endpoint returns the sample response")
def step_notes_returns_sample(context):
    context.respx_mock.get(_notes_url(context)).mock(
        return_value=httpx.Response(200, json=load_sample("api/v1/notes"))
    )


@given("the Substack notes endpoint returns status {status:d}")
def step_notes_returns_status(context, status):
    context.respx_mock.get(_notes_url(context)).mock(
        return_value=httpx.Response(status)
    )


@given("the Substack posts endpoint returns the sample response for user {user_id:d}")
def step_posts_returns_sample(context, user_id):
    context.respx_mock.get(_profile_posts_url()).mock(
        return_value=httpx.Response(200, json=load_sample("api/v1/profile/posts"))
    )


@given("the Substack user-settings endpoint returns user id {user_id:d}")
def step_user_setting_returns_user_id(context, user_id):
    context.respx_mock.get(user_setting_url()).mock(
        return_value=httpx.Response(
            200,
            json={
                "userSettings": [
                    {
                        "user_id": user_id,
                        "type": "last_home_tab",
                        "value_bool": None,
                        "value_datetime": None,
                        "value_integer": None,
                        "value_text": "inbox",
                    }
                ],
                "qualifiesForBadge": False,
            },
        )
    )


@given("the Substack user-settings endpoint returns status {status:d}")
def step_user_setting_returns_status(context, status):
    context.respx_mock.get(user_setting_url()).mock(return_value=httpx.Response(status))


@given(
    "the Substack subscriber-lists endpoint returns the sample response for user {user_id:d}"
)
def step_subscriber_lists_returns_sample(context, user_id):
    context.respx_mock.get(_subscriber_lists_url(context, user_id)).mock(
        return_value=httpx.Response(
            200,
            json=load_sample(f"api/v1/user/{user_id}/subscriber-lists"),
        )
    )
