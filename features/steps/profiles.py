from __future__ import annotations

import httpx
from behave import given

_SUBSTACK_BASE = "https://substack.com"
_PUBLIC_PROFILE_PATH = "/api/v1/user/{slug}/public_profile"


def _public_profile_url(slug: str) -> str:
    return f"{_SUBSTACK_BASE}{_PUBLIC_PROFILE_PATH.format(slug=slug)}"


@given('the Substack public profile endpoint for "{slug}" returns status {status:d}')
def step_public_profile_returns_status(context, slug, status):
    context.respx_mock.get(_public_profile_url(slug)).mock(
        return_value=httpx.Response(status)
    )
