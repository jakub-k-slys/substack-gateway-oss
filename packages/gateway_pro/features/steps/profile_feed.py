from __future__ import annotations

import httpx
from behave import given, then
from common import public_profile_url
from common_shim import SUBSTACK_BASE, load_sample


def _profile_feed_notes_url(profile_id: int) -> str:
    return f"{SUBSTACK_BASE}/api/v1/reader/feed/profile/{profile_id}"


def _profile_feed_posts_url(profile_id: int) -> str:
    return f"{SUBSTACK_BASE}/api/v1/profile/posts"


def _full_post_url(post_id: int) -> str:
    return f"{SUBSTACK_BASE}/api/v1/posts/by-id/{post_id}"


@given(
    "the Substack profile feed-notes endpoint returns the sample response for user {profile_id:d}"
)
def step_profile_feed_notes_returns_sample(context, profile_id):
    context.respx_mock.get(_profile_feed_notes_url(profile_id)).mock(
        return_value=httpx.Response(
            200,
            json=load_sample(f"api/v1/feed/profile/{profile_id}?types=note"),
        )
    )


@given(
    "the Substack profile feed-posts endpoint returns the sample response for user {profile_id:d}"
)
def step_profile_feed_posts_returns_sample(context, profile_id):
    context.respx_mock.get(_profile_feed_posts_url(profile_id)).mock(
        return_value=httpx.Response(
            200,
            json=load_sample("api/v1/profile/posts"),
        )
    )


@given(
    "the Substack full post endpoint returns the sample response for post {post_id:d}"
)
def step_full_post_returns_sample(context, post_id):
    context.respx_mock.get(_full_post_url(post_id)).mock(
        return_value=httpx.Response(
            200,
            json=load_sample(f"api/v1/posts/by-id/{post_id}"),
        )
    )


@given('the Substack public profile endpoint for "{slug}" returns status {status:d}')
def step_public_profile_returns_status(context, slug, status):
    context.respx_mock.get(public_profile_url(slug)).mock(
        return_value=httpx.Response(status)
    )


@then('the response content type starts with "{value}"')
def step_response_content_type_starts_with(context, value):
    actual = context.response.headers["content-type"]
    assert actual.startswith(value), (
        f'Expected content-type to start with "{value}", got "{actual}"'
    )
