from __future__ import annotations

import httpx
from behave import given

_SUBSTACK_BASE = "https://substack.com"
_HANDLE_OPTIONS_PATH = "/api/v1/handle/options"
_PUBLIC_PROFILE_PATH = "/api/v1/user/{slug}/public_profile"


def _handle_options_url(context) -> str:
    pub_url = context.headers.get("x-publication-url", "").rstrip("/")
    return f"{pub_url}{_HANDLE_OPTIONS_PATH}"


def _public_profile_url(slug: str) -> str:
    return f"{_SUBSTACK_BASE}{_PUBLIC_PROFILE_PATH.format(slug=slug)}"


@given('the Substack handles endpoint returns handle "{handle}"')
def step_handles_returns_handle(context, handle):
    context.respx_mock.get(_handle_options_url(context)).mock(
        return_value=httpx.Response(200, json=[{"handle": handle}])
    )


@given('the Substack public profile endpoint returns a profile for "{handle}"')
def step_public_profile_returns(context, handle):
    context.respx_mock.get(_public_profile_url(handle)).mock(
        return_value=httpx.Response(
            200,
            json={
                "id": 42,
                "handle": handle,
                "name": "Test User",
                "photo_url": "https://example.com/avatar.jpg",
                "bio": "A test bio",
            },
        )
    )


@given("the Substack handles endpoint returns status {status:d}")
def step_handles_returns_status(context, status):
    context.respx_mock.get(_handle_options_url(context)).mock(
        return_value=httpx.Response(status)
    )
