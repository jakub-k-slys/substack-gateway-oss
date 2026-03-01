"""Behave step definitions for MCP tool testing.

MCP tools are async functions, so each When step calls asyncio.run() to
execute the coroutine from synchronous behave.  The respx mock started in
environment.py patches httpx at the class level, so it remains active
across asyncio.run() boundaries.

The valid-token Given step also writes context.headers["x-publication-url"]
so that the shared Substack mock Given steps (drafts.py, reader.py,
notes_create.py) can derive the correct URL to register mocks against.
"""

from __future__ import annotations

import asyncio
import base64
import json

from behave import given, then, when

from gateway.mcp.app import (
    create_draft,
    create_note,
    delete_draft,
    delete_note,
    get_draft,
    get_me,
    get_my_notes,
    get_my_posts,
    get_note,
    get_post,
)


# ------------------------------------------------------------------
# Given — authentication
# ------------------------------------------------------------------


@given('a valid MCP token and publication URL "{pub_url_}"')
def step_valid_mcp_token(context, pub_url_):
    credentials = {"substack_sid": "test-token", "connect_sid": "test-token"}
    encoded = base64.b64encode(json.dumps(credentials).encode()).decode()
    context.mcp_token = encoded
    context.mcp_pub_url = pub_url_
    # Keep headers in sync so existing Substack mock Given steps work.
    context.headers["x-publication-url"] = pub_url_


@given('an invalid MCP token and publication URL "{pub_url_}"')
def step_invalid_mcp_token(context, pub_url_):
    context.mcp_token = "not-valid-base64!!!"
    context.mcp_pub_url = pub_url_
    context.headers["x-publication-url"] = pub_url_


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _call(context, coro):
    """Run an async coroutine, capturing result or exception into context."""
    try:
        context.mcp_result = asyncio.run(coro)
        context.mcp_error = None
    except Exception as exc:  # noqa: BLE001
        context.mcp_result = None
        context.mcp_error = exc


# ------------------------------------------------------------------
# When — notes
# ------------------------------------------------------------------


@when("I call the MCP tool get_note with note_id {note_id:d}")
def step_call_get_note(context, note_id):
    _call(
        context,
        get_note(
            note_id=note_id,
            token=context.mcp_token,
            publication_url=context.mcp_pub_url,
        ),
    )


@when('I call the MCP tool create_note with content "{content}"')
def step_call_create_note(context, content):
    _call(
        context,
        create_note(
            content=content,
            token=context.mcp_token,
            publication_url=context.mcp_pub_url,
        ),
    )


@when("I call the MCP tool delete_note with note_id {note_id:d}")
def step_call_delete_note(context, note_id):
    _call(
        context,
        delete_note(
            note_id=note_id,
            token=context.mcp_token,
            publication_url=context.mcp_pub_url,
        ),
    )


# ------------------------------------------------------------------
# When — drafts
# ------------------------------------------------------------------


@when("I call the MCP tool get_draft with draft_id {draft_id:d}")
def step_call_get_draft(context, draft_id):
    _call(
        context,
        get_draft(
            draft_id=draft_id,
            token=context.mcp_token,
            publication_url=context.mcp_pub_url,
        ),
    )


@when('I call the MCP tool create_draft with title "{title}"')
def step_call_create_draft(context, title):
    _call(
        context,
        create_draft(
            title=title,
            token=context.mcp_token,
            publication_url=context.mcp_pub_url,
        ),
    )


@when("I call the MCP tool delete_draft with draft_id {draft_id:d}")
def step_call_delete_draft(context, draft_id):
    _call(
        context,
        delete_draft(
            draft_id=draft_id,
            token=context.mcp_token,
            publication_url=context.mcp_pub_url,
        ),
    )


# ------------------------------------------------------------------
# When — me / posts
# ------------------------------------------------------------------


@when("I call the MCP tool get_me")
def step_call_get_me(context):
    _call(
        context,
        get_me(token=context.mcp_token, publication_url=context.mcp_pub_url),
    )


@when("I call the MCP tool get_my_notes")
def step_call_get_my_notes(context):
    _call(
        context,
        get_my_notes(token=context.mcp_token, publication_url=context.mcp_pub_url),
    )


@when("I call the MCP tool get_my_posts")
def step_call_get_my_posts(context):
    _call(
        context,
        get_my_posts(token=context.mcp_token, publication_url=context.mcp_pub_url),
    )


@when("I call the MCP tool get_post with post_id {post_id:d}")
def step_call_get_post(context, post_id):
    _call(
        context,
        get_post(
            post_id=post_id,
            token=context.mcp_token,
            publication_url=context.mcp_pub_url,
        ),
    )


# ------------------------------------------------------------------
# Then — assertions
# ------------------------------------------------------------------


@then('the MCP result field "{field}" is not null')
def step_mcp_field_not_null(context, field):
    assert context.mcp_error is None, f"MCP tool raised: {context.mcp_error}"
    assert context.mcp_result[field] is not None, (
        f'Expected "{field}" to be non-null, got null'
    )


@then('the MCP result field "{field}" is "{value}"')
def step_mcp_field_string(context, field, value):
    assert context.mcp_error is None, f"MCP tool raised: {context.mcp_error}"
    actual = context.mcp_result[field]
    assert actual == value, f'Expected "{field}" to be "{value}", got "{actual}"'


@then('the MCP result is "{value}"')
def step_mcp_result_string(context, value):
    assert context.mcp_error is None, f"MCP tool raised: {context.mcp_error}"
    assert context.mcp_result == value, (
        f'Expected result to be "{value}", got "{context.mcp_result}"'
    )


@then("the MCP tool raises a ValueError")
def step_mcp_raises_value_error(context):
    assert isinstance(context.mcp_error, ValueError), (
        f"Expected ValueError, got {type(context.mcp_error).__name__}: {context.mcp_error}"
    )
