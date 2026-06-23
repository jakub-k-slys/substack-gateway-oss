from __future__ import annotations

import httpx
from behave import given
from common import SUBSTACK_BASE, load_sample, pub_url


def _full_post_url(post_id: int) -> str:
    return f"{SUBSTACK_BASE}/api/v1/posts/by-id/{post_id}"


def _post_comments_url(context, post_id: int) -> str:
    return f"{pub_url(context)}/api/v1/post/{post_id}/comments"


@given(
    "the Substack full post endpoint returns the sample response for post {post_id:d}"
)
def step_full_post_returns_sample(context, post_id):
    context.respx_mock.get(_full_post_url(post_id)).mock(
        return_value=httpx.Response(
            200, json=load_sample(f"api/v1/posts/by-id/{post_id}")
        )
    )


@given("the Substack full post endpoint for post {post_id:d} returns status {status:d}")
def step_full_post_returns_status(context, post_id, status):
    context.respx_mock.get(_full_post_url(post_id)).mock(
        return_value=httpx.Response(status)
    )


@given(
    "the Substack comments endpoint returns the sample response for post {post_id:d}"
)
def step_post_comments_returns_sample(context, post_id):
    context.respx_mock.get(_post_comments_url(context, post_id)).mock(
        return_value=httpx.Response(
            200, json=load_sample(f"api/v1/post/{post_id}/comments")
        )
    )


@given("the Substack comments endpoint for post {post_id:d} returns status {status:d}")
def step_post_comments_returns_status(context, post_id, status):
    context.respx_mock.get(_post_comments_url(context, post_id)).mock(
        return_value=httpx.Response(status)
    )
