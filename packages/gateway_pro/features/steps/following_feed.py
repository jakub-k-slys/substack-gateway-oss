from __future__ import annotations

import httpx
from behave import given
from common import SUBSTACK_BASE
from common_shim import load_sample


def _profile_feed_notes_url(profile_id: int) -> str:
    return f"{SUBSTACK_BASE}/api/v1/reader/feed/profile/{profile_id}"


def _profile_feed_posts_url() -> str:
    return f"{SUBSTACK_BASE}/api/v1/profile/posts"


@given(
    'the Substack followed profile notes endpoint returns a sample response for user {user_id:d} with handle "{handle}"'
)
def step_followed_profile_notes_returns_sample(context, user_id, handle):
    context.respx_mock.get(_profile_feed_notes_url(user_id)).mock(
        return_value=httpx.Response(
            200,
            json=load_sample(f"api/v1/feed/profile/{user_id}?types=note"),
        )
    )


@given(
    'the Substack followed profile posts endpoint returns a sample response for user {user_id:d} with title "{title}"'
)
def step_followed_profile_posts_returns_sample(context, user_id, title):
    context.respx_mock.get(
        _profile_feed_posts_url(),
        params={"profile_user_id": str(user_id), "limit": "3"},
    ).mock(
        return_value=httpx.Response(
            200,
            json=load_sample(f"api/v1/profile/posts?profile_user_id={user_id}&limit=3"),
        )
    )
