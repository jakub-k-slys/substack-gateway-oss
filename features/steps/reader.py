from __future__ import annotations

import json
import pathlib

import httpx
from behave import given

_SUBSTACK_BASE = "https://substack.com"

_SAMPLES_DIR = pathlib.Path(__file__).parent.parent.parent / "samples"


def _load_sample(path: str):
    return json.loads((_SAMPLES_DIR / path).read_text())


def _reader_comment_url(comment_id: int) -> str:
    return f"{_SUBSTACK_BASE}/api/v1/reader/comment/{comment_id}"


@given(
    "the Substack reader comment endpoint returns the sample response for id {comment_id:d}"
)
def step_reader_comment_returns_sample(context, comment_id):
    context.respx_mock.get(_reader_comment_url(comment_id)).mock(
        return_value=httpx.Response(
            200, json=_load_sample(f"api/v1/reader/comment/{comment_id}")
        )
    )


@given(
    "the Substack reader comment endpoint for id {comment_id:d} returns status {status:d}"
)
def step_reader_comment_returns_status(context, comment_id, status):
    context.respx_mock.get(_reader_comment_url(comment_id)).mock(
        return_value=httpx.Response(status)
    )
