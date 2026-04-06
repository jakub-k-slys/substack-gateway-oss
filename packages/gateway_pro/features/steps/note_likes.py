from __future__ import annotations

import httpx
from behave import given, when
from common_shim import SUBSTACK_BASE


def _note_reaction_url(note_id: int) -> str:
    return f"{SUBSTACK_BASE}/api/v1/comment/{note_id}/reaction"


@given("the Substack like-note endpoint returns status {status:d} for note {note_id:d}")
def step_like_note_returns_status(context, status, note_id):
    context.respx_mock.post(_note_reaction_url(note_id)).mock(
        return_value=httpx.Response(status)
    )


@given(
    "the Substack unlike-note endpoint returns status {status:d} for note {note_id:d}"
)
def step_unlike_note_returns_status(context, status, note_id):
    context.respx_mock.delete(_note_reaction_url(note_id)).mock(
        return_value=httpx.Response(status)
    )


@when("I send PUT {path}")
def step_send_put(context, path):
    context.response = context.client.put(path, headers=context.headers)
