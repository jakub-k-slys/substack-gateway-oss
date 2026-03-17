from __future__ import annotations

import httpx
from behave import given

from packages.gateway_oss.features.steps.common import (
    load_sample,
    pub_url,
    public_profile_url,
)

_PROFILE_NOTES_PATH = "/api/v1/reader/feed/profile/{profile_id}"


def _profile_notes_url(context, profile_id: int) -> str:
    return f"{pub_url(context)}{_PROFILE_NOTES_PATH.format(profile_id=profile_id)}"


@given('the Substack public profile endpoint for "{slug}" returns status {status:d}')
def step_public_profile_returns_status(context, slug, status):
    context.respx_mock.get(public_profile_url(slug)).mock(
        return_value=httpx.Response(status)
    )


@given(
    'the Substack public profile endpoint for "{slug}" returns a response with no id field'
)
def step_public_profile_returns_no_id(context, slug):
    context.respx_mock.get(public_profile_url(slug)).mock(
        return_value=httpx.Response(200, json={"handle": slug, "name": "Test"})
    )


@given(
    'the Substack public profile endpoint for "{slug}" returns a response with a non-integer id'
)
def step_public_profile_returns_bad_id(context, slug):
    context.respx_mock.get(public_profile_url(slug)).mock(
        return_value=httpx.Response(
            200, json={"id": "not-a-number", "handle": slug, "name": "Test"}
        )
    )


@given(
    "the Substack profile notes endpoint returns the sample response for user {profile_id:d}"
)
def step_profile_notes_returns_sample(context, profile_id):
    context.respx_mock.get(_profile_notes_url(context, profile_id)).mock(
        return_value=httpx.Response(
            200,
            json=load_sample(f"api/v1/feed/profile/{profile_id}?types=note"),
        )
    )


@given(
    "the Substack profile notes endpoint for user {profile_id:d} returns status {status:d}"
)
def step_profile_notes_returns_status(context, profile_id, status):
    context.respx_mock.get(_profile_notes_url(context, profile_id)).mock(
        return_value=httpx.Response(status)
    )
