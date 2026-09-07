from __future__ import annotations

import httpx
from behave import given
from common import SUBSTACK_BASE


def _post_reaction_url(post_id: int) -> str:
    return f"{SUBSTACK_BASE}/api/v1/post/{post_id}/reaction"


def _post_restack_url() -> str:
    return f"{SUBSTACK_BASE}/api/v1/restack/feed"


@given("the Substack like-post endpoint returns status {status:d} for post {post_id:d}")
def step_like_post_returns_status(context, status, post_id):
    context.respx_mock.post(_post_reaction_url(post_id)).mock(
        return_value=httpx.Response(status)
    )


@given(
    "the Substack unlike-post endpoint returns status {status:d} for post {post_id:d}"
)
def step_unlike_post_returns_status(context, status, post_id):
    context.respx_mock.delete(_post_reaction_url(post_id)).mock(
        return_value=httpx.Response(status)
    )


@given("the Substack restack-post endpoint returns status {status:d}")
def step_restack_post_returns_status(context, status):
    context.respx_mock.post(_post_restack_url()).mock(
        return_value=httpx.Response(status)
    )
