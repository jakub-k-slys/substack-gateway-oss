from __future__ import annotations

import json
import pathlib

import httpx
from behave import given

_SUBSTACK_BASE = "https://substack.com"

_SAMPLES_DIR = pathlib.Path(__file__).parent.parent.parent / "samples"


def _load_sample(path: str):
    return json.loads((_SAMPLES_DIR / path).read_text())


def _full_post_url(post_id: int) -> str:
    return f"{_SUBSTACK_BASE}/api/v1/posts/by-id/{post_id}"


def _post_comments_url(context, post_id: int) -> str:
    pub_url = context.headers.get("x-publication-url", "").rstrip("/")
    return f"{pub_url}/api/v1/post/{post_id}/comments"


@given(
    "the Substack full post endpoint returns the sample response for post {post_id:d}"
)
def step_full_post_returns_sample(context, post_id):
    context.respx_mock.get(_full_post_url(post_id)).mock(
        return_value=httpx.Response(
            200, json=_load_sample(f"api/v1/posts/by-id/{post_id}")
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
            200, json=_load_sample(f"api/v1/post/{post_id}/comments")
        )
    )


@given("the Substack comments endpoint for post {post_id:d} returns status {status:d}")
def step_post_comments_returns_status(context, post_id, status):
    context.respx_mock.get(_post_comments_url(context, post_id)).mock(
        return_value=httpx.Response(status)
    )
