from __future__ import annotations

import httpx
from behave import given
from common import load_sample, pub_url


def _detail_url(context, post_id: int, tab: str) -> str:
    return f"{pub_url(context)}/api/v1/post_management/detail/{post_id}/{tab}"


@given(
    "the Substack post {tab} endpoint returns the sample response for post {post_id:d}"
)
def step_post_stats_sample(context, tab, post_id):
    context.respx_mock.get(_detail_url(context, post_id, tab)).mock(
        return_value=httpx.Response(200, json=load_sample(f"api/v1/post-stats/{tab}"))
    )


@given(
    "the Substack post {tab} endpoint returns status {status:d} for post {post_id:d}"
)
def step_post_stats_status(context, tab, status, post_id):
    context.respx_mock.get(_detail_url(context, post_id, tab)).mock(
        return_value=httpx.Response(status)
    )
