from __future__ import annotations

import httpx
from behave import given
from packages.gateway_oss.features.steps.common import SUBSTACK_BASE, load_sample

_CREATE_NOTE_URL = f"{SUBSTACK_BASE}/api/v1/comment/feed/"
_CREATE_ATTACHMENT_URL = f"{SUBSTACK_BASE}/api/v1/comment/attachment/"


def _delete_note_url(context, note_id: int) -> str:
    pub = context.headers.get("x-publication-url")
    if not pub:
        raise RuntimeError("x-publication-url not set — missing a Given step?")
    return f"{pub.rstrip('/')}/api/v1/comment/{note_id}"


@given("the Substack create-note endpoint returns the sample response")
def step_create_note_returns_sample(context):
    context.respx_mock.post(_CREATE_NOTE_URL).mock(
        return_value=httpx.Response(200, json=load_sample("api/v1/comment/response"))
    )


@given("the Substack create-note endpoint returns status {status:d}")
def step_create_note_returns_status(context, status):
    context.respx_mock.post(_CREATE_NOTE_URL).mock(return_value=httpx.Response(status))


@given("the Substack create-attachment endpoint returns the sample response")
def step_create_attachment_returns_sample(context):
    context.respx_mock.post(_CREATE_ATTACHMENT_URL).mock(
        return_value=httpx.Response(
            200, json=load_sample("api/v1/comment/attachment-response")
        )
    )


@given("the Substack create-attachment endpoint returns status {status:d}")
def step_create_attachment_returns_status(context, status):
    context.respx_mock.post(_CREATE_ATTACHMENT_URL).mock(
        return_value=httpx.Response(status)
    )


@given(
    "the Substack delete-note endpoint returns status {status:d} for note {note_id:d}"
)
def step_delete_note_returns_status(context, status, note_id):
    context.respx_mock.delete(_delete_note_url(context, note_id)).mock(
        return_value=httpx.Response(status)
    )
