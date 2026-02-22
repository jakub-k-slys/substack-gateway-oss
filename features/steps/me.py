from __future__ import annotations

import json
import pathlib

import httpx
from behave import given

_SUBSTACK_BASE = "https://substack.com"
_HANDLE_OPTIONS_PATH = "/api/v1/handle/options"
_PUBLIC_PROFILE_PATH = "/api/v1/user/{slug}/public_profile"

_SAMPLES_DIR = pathlib.Path(__file__).parent.parent.parent / "samples"


def _load_sample(path: str):
    return json.loads((_SAMPLES_DIR / path).read_text())


def _handle_options_url(context) -> str:
    pub_url = context.headers.get("x-publication-url", "").rstrip("/")
    return f"{pub_url}{_HANDLE_OPTIONS_PATH}"


def _public_profile_url(slug: str) -> str:
    return f"{_SUBSTACK_BASE}{_PUBLIC_PROFILE_PATH.format(slug=slug)}"


@given("the Substack handles endpoint returns the sample response")
def step_handles_returns_sample(context):
    context.respx_mock.get(_handle_options_url(context)).mock(
        return_value=httpx.Response(200, json=_load_sample("api/v1/handle/options"))
    )


@given(
    'the Substack public profile endpoint returns the sample response for "{handle}"'
)
def step_public_profile_returns_sample(context, handle):
    context.respx_mock.get(_public_profile_url(handle)).mock(
        return_value=httpx.Response(
            200, json=_load_sample(f"api/v1/user/{handle}/public_profile")
        )
    )


@given("the Substack handles endpoint returns status {status:d}")
def step_handles_returns_status(context, status):
    context.respx_mock.get(_handle_options_url(context)).mock(
        return_value=httpx.Response(status)
    )


def _notes_url(context) -> str:
    pub_url = context.headers.get("x-publication-url", "").rstrip("/")
    return f"{pub_url}/api/v1/notes"


def _profile_posts_url(context) -> str:
    pub_url = context.headers.get("x-publication-url", "").rstrip("/")
    return f"{pub_url}/api/v1/profile/posts"


@given("the Substack notes endpoint returns the sample response")
def step_notes_returns_sample(context):
    context.respx_mock.get(_notes_url(context)).mock(
        return_value=httpx.Response(200, json=_load_sample("api/v1/notes"))
    )


@given("the Substack notes endpoint returns status {status:d}")
def step_notes_returns_status(context, status):
    context.respx_mock.get(_notes_url(context)).mock(
        return_value=httpx.Response(status)
    )


@given("the Substack posts endpoint returns the sample response for user {user_id:d}")
def step_posts_returns_sample(context, user_id):
    context.respx_mock.get(_profile_posts_url(context)).mock(
        return_value=httpx.Response(200, json=_load_sample("api/v1/profile/posts"))
    )


def _user_setting_url(context) -> str:
    pub_url = context.headers.get("x-publication-url", "").rstrip("/")
    return f"{pub_url}/api/v1/user-setting"


def _subscriber_lists_url(context, user_id: int) -> str:
    pub_url = context.headers.get("x-publication-url", "").rstrip("/")
    return f"{pub_url}/api/v1/user/{user_id}/subscriber-lists"


@given("the Substack user-setting endpoint returns user id {user_id:d}")
def step_user_setting_returns_user_id(context, user_id):
    context.respx_mock.put(_user_setting_url(context)).mock(
        return_value=httpx.Response(200, json=_load_sample("api/v1/user-setting"))
    )


@given("the Substack user-setting endpoint returns status {status:d}")
def step_user_setting_returns_status(context, status):
    context.respx_mock.put(_user_setting_url(context)).mock(
        return_value=httpx.Response(status)
    )


@given(
    "the Substack subscriber-lists endpoint returns the sample response for user {user_id:d}"
)
def step_subscriber_lists_returns_sample(context, user_id):
    context.respx_mock.get(_subscriber_lists_url(context, user_id)).mock(
        return_value=httpx.Response(
            200,
            json=_load_sample(f"api/v1/user/{user_id}/subscriber-lists"),
        )
    )
