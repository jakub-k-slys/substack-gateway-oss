from __future__ import annotations

import httpx
from behave import given, when
from common import pub_url


def _post_comment_url(context, post_id):
    return f"{pub_url(context)}/api/v1/post/{post_id}/comment"


def _reader_comment_url(context, comment_id):
    return f"{pub_url(context)}/api/v1/reader/comment/{comment_id}"


def _reader_replies_url(context, comment_id):
    return f"{pub_url(context)}/api/v1/reader/comment/{comment_id}/replies"


def _comment_url(context, comment_id):
    return f"{pub_url(context)}/api/v1/comment/{comment_id}"


def _reaction_url(context, comment_id):
    return f"{pub_url(context)}/api/v1/comment/{comment_id}/reaction"


@given("the Substack post comment endpoint for post {post_id:d} returns id {new_id:d}")
def step_create_comment_ok(context, post_id, new_id):
    context.respx_mock.post(_post_comment_url(context, post_id)).mock(
        return_value=httpx.Response(200, json={"id": new_id, "body": "hello"})
    )


@given(
    "the Substack reader comment endpoint for id {comment_id:d} "
    "resolves to post {post_id:d}"
)
def step_reader_resolves_post(context, comment_id, post_id):
    context.respx_mock.get(_reader_comment_url(context, comment_id)).mock(
        return_value=httpx.Response(
            200,
            json={
                "item": {
                    "entity_key": "k",
                    "context": {
                        "timestamp": "2024-01-15T10:00:00.000Z",
                        "users": [],
                    },
                    "post": {
                        "id": post_id,
                        "title": "Parent post",
                        "post_date": "2024-01-15T10:00:00.000Z",
                    },
                    "comment": {
                        "id": comment_id,
                        "body": "parent",
                        "name": "Ann",
                        "reaction_count": 1,
                    },
                }
            },
        )
    )


@given("the Substack comment reply endpoint for post {post_id:d} returns id {new_id:d}")
def step_reply_ok(context, post_id, new_id):
    context.respx_mock.post(_post_comment_url(context, post_id)).mock(
        return_value=httpx.Response(200, json={"id": new_id, "body": "re"})
    )


@given(
    "the Substack comment replies endpoint for id {comment_id:d} returns two replies"
)
def step_replies_ok(context, comment_id):
    context.respx_mock.get(_reader_replies_url(context, comment_id)).mock(
        return_value=httpx.Response(
            200,
            json={
                "commentBranches": [
                    {"comment": {"id": 1, "body": "a"}},
                    {"comment": {"id": 2, "body": "b"}},
                ]
            },
        )
    )


@given(
    "the Substack delete comment endpoint for id {comment_id:d} returns status {status:d}"
)
def step_delete_ok(context, comment_id, status):
    context.respx_mock.delete(_comment_url(context, comment_id)).mock(
        return_value=httpx.Response(status)
    )


@given("the Substack comment reaction endpoint for id {comment_id:d} accepts a like")
def step_like_ok(context, comment_id):
    context.respx_mock.post(_reaction_url(context, comment_id)).mock(
        return_value=httpx.Response(200, json={"ok": True})
    )


@given("the Substack comment reaction endpoint for id {comment_id:d} accepts an unlike")
def step_unlike_ok(context, comment_id):
    context.respx_mock.delete(_reaction_url(context, comment_id)).mock(
        return_value=httpx.Response(200, json={"ok": True})
    )


@when("I send POST {path}")
def step_post_no_body(context, path):
    context.response = context.client.post(path, headers=context.headers)
