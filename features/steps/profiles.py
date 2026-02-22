from __future__ import annotations

import json
import pathlib

import httpx
from behave import given

_SUBSTACK_BASE = "https://substack.com"
_PUBLIC_PROFILE_PATH = "/api/v1/user/{slug}/public_profile"
_PROFILE_NOTES_PATH = "/api/v1/reader/feed/profile/{profile_id}"

_SAMPLES_DIR = pathlib.Path(__file__).parent.parent.parent / "samples"


def _load_sample(path: str):
    return json.loads((_SAMPLES_DIR / path).read_text())


def _public_profile_url(slug: str) -> str:
    return f"{_SUBSTACK_BASE}{_PUBLIC_PROFILE_PATH.format(slug=slug)}"


def _profile_notes_url(profile_id: int) -> str:
    return f"{_SUBSTACK_BASE}{_PROFILE_NOTES_PATH.format(profile_id=profile_id)}"


@given('the Substack public profile endpoint for "{slug}" returns status {status:d}')
def step_public_profile_returns_status(context, slug, status):
    context.respx_mock.get(_public_profile_url(slug)).mock(
        return_value=httpx.Response(status)
    )


@given(
    "the Substack profile notes endpoint returns the sample response for user {profile_id:d}"
)
def step_profile_notes_returns_sample(context, profile_id):
    context.respx_mock.get(_profile_notes_url(profile_id)).mock(
        return_value=httpx.Response(
            200,
            json=_load_sample("api/v1/feed/profile/343074721?types=note"),
        )
    )


@given(
    "the Substack profile notes endpoint for user {profile_id:d} returns status {status:d}"
)
def step_profile_notes_returns_status(context, profile_id, status):
    context.respx_mock.get(_profile_notes_url(profile_id)).mock(
        return_value=httpx.Response(status)
    )
