from __future__ import annotations

import httpx
from behave import given, when
from common import SUBSTACK_BASE


def _reaction_url(note_id: int) -> str:
    return f"{SUBSTACK_BASE}/api/v1/comment/{note_id}/reaction"


def _reply_feed_url() -> str:
    return f"{SUBSTACK_BASE}/api/v1/comment/feed/"


def _replies_url(note_id: int) -> str:
    return f"{SUBSTACK_BASE}/api/v1/reader/comment/{note_id}/replies"


@given("the Substack like-note endpoint returns status {status:d} for note {note_id:d}")
def step_like_note_status(context, status, note_id):
    context.respx_mock.post(_reaction_url(note_id)).mock(
        return_value=httpx.Response(status)
    )


@given(
    "the Substack unlike-note endpoint returns status {status:d} for note {note_id:d}"
)
def step_unlike_note_status(context, status, note_id):
    context.respx_mock.delete(_reaction_url(note_id)).mock(
        return_value=httpx.Response(status)
    )


@given("the Substack note-reply endpoint returns id {reply_id:d}")
def step_note_reply_returns_id(context, reply_id):
    context.respx_mock.post(_reply_feed_url()).mock(
        return_value=httpx.Response(
            200, json={"id": reply_id, "date": "2026-08-04", "status": "published"}
        )
    )


@given("the Substack note-replies endpoint returns two replies for note {note_id:d}")
def step_note_replies_returns_two(context, note_id):
    context.respx_mock.get(_replies_url(note_id)).mock(
        return_value=httpx.Response(
            200,
            json={
                "commentBranches": [
                    {"comment": {"id": 1, "body": "first"}},
                    {"comment": {"id": 2, "body": "second"}},
                ]
            },
        )
    )


@when("I send PUT {path}")
def step_send_put_no_body(context, path):
    context.response = context.client.put(path, headers=context.headers)
