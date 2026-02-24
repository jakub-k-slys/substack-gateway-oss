from __future__ import annotations

import httpx
from behave import given

from features.steps.common import SUBSTACK_BASE, load_sample

_CREATE_NOTE_URL = f"{SUBSTACK_BASE}/api/v1/comment/feed/"


@given("the Substack create-note endpoint returns the sample response")
def step_create_note_returns_sample(context):
    context.respx_mock.post(_CREATE_NOTE_URL).mock(
        return_value=httpx.Response(200, json=load_sample("api/v1/comment/response"))
    )


@given("the Substack create-note endpoint returns status {status:d}")
def step_create_note_returns_status(context, status):
    context.respx_mock.post(_CREATE_NOTE_URL).mock(return_value=httpx.Response(status))
