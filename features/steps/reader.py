from __future__ import annotations

import httpx
from behave import given

from features.steps.common import load_sample, pub_url


def _reader_comment_url(context, comment_id: int) -> str:
    return f"{pub_url(context)}/api/v1/reader/comment/{comment_id}"


@given(
    "the Substack reader comment endpoint returns the sample response for id {comment_id:d}"
)
def step_reader_comment_returns_sample(context, comment_id):
    context.respx_mock.get(_reader_comment_url(context, comment_id)).mock(
        return_value=httpx.Response(
            200, json=load_sample(f"api/v1/reader/comment/{comment_id}")
        )
    )


@given(
    "the Substack reader comment endpoint for id {comment_id:d} returns status {status:d}"
)
def step_reader_comment_returns_status(context, comment_id, status):
    context.respx_mock.get(_reader_comment_url(context, comment_id)).mock(
        return_value=httpx.Response(status)
    )
