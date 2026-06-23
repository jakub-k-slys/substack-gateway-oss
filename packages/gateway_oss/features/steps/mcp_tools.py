"""Behave step definitions for OSS and PRO MCP tool testing.

Public OSS tools run without credentials. PRO-only personal/write tools still
use the authenticated helper path.
"""

from __future__ import annotations

import asyncio
import base64
import json

from behave import given, then, when

from gateway_oss.mcp.app import (
    create_note,
    delete_note,
    get_me,
    get_my_following,
    get_my_notes,
    get_my_posts,
    get_note,
    get_post,
    get_post_comments,
    get_profile,
    get_profile_notes,
    get_profile_posts,
)

# ------------------------------------------------------------------
# Given — authentication
# ------------------------------------------------------------------


@given('a valid MCP token and publication URL "{pub_url_}"')
def step_valid_mcp_token(context, pub_url_):
    credentials = {
        "publication_url": pub_url_,
        "substack_sid": "test-token",
        "connect_sid": "test-token",
    }
    encoded = base64.b64encode(json.dumps(credentials).encode()).decode()
    context.mcp_token = encoded
    context.mcp_pub_url = pub_url_
    context.publication_url = pub_url_


@given('an invalid MCP token and publication URL "{pub_url_}"')
def step_invalid_mcp_token(context, pub_url_):
    context.mcp_token = "not-valid-base64!!!"
    context.mcp_pub_url = pub_url_
    context.publication_url = pub_url_


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


@when("I call the MCP tool get_note with note_id {note_id:d}")
def step_call_get_note(context, note_id):
    _call(context, get_note(note_id=note_id, token=context.mcp_token))


@when('I call the MCP tool create_note with content "{content}"')
def step_call_create_note(context, content):
    _call(context, create_note(content=content, token=context.mcp_token))


@when("I call the MCP tool delete_note with note_id {note_id:d}")
def step_call_delete_note(context, note_id):
    _call(context, delete_note(note_id=note_id, token=context.mcp_token))


# ------------------------------------------------------------------
# When — me / posts
# ------------------------------------------------------------------


@when("I call the MCP tool get_me")
def step_call_get_me(context):
    _call(context, get_me(token=context.mcp_token))


@when("I call the MCP tool get_my_notes")
def step_call_get_my_notes(context):
    _call(context, get_my_notes(token=context.mcp_token))


@when("I call the MCP tool get_my_posts")
def step_call_get_my_posts(context):
    _call(context, get_my_posts(token=context.mcp_token))


@when("I call the MCP tool get_post with post_id {post_id:d}")
def step_call_get_post(context, post_id):
    _call(context, get_post(post_id=post_id, token=context.mcp_token))


@when("I call the MCP tool get_post_comments with post_id {post_id:d}")
def step_call_get_post_comments(context, post_id):
    _call(context, get_post_comments(post_id=post_id, token=context.mcp_token))


@when("I call the MCP tool get_my_following")
def step_call_get_my_following(context):
    _call(context, get_my_following(token=context.mcp_token))


# ------------------------------------------------------------------
# When — profiles
# ------------------------------------------------------------------


@when('I call the MCP tool get_profile with slug "{slug}"')
def step_call_get_profile(context, slug):
    _call(context, get_profile(slug=slug))


@when('I call the MCP tool get_profile_posts with slug "{slug}"')
def step_call_get_profile_posts(context, slug):
    _call(context, get_profile_posts(slug=slug))


@when('I call the MCP tool get_profile_notes with slug "{slug}"')
def step_call_get_profile_notes(context, slug):
    _call(context, get_profile_notes(slug=slug))


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


@then('the MCP result list "{field}" has {count:d} items')
def step_mcp_list_count(context, field, count):
    assert context.mcp_error is None, f"MCP tool raised: {context.mcp_error}"
    actual = context.mcp_result[field]
    assert isinstance(actual, list), f'Expected "{field}" to be a list'
    assert len(actual) == count, f"Expected {count} items, got {len(actual)}"


@then('the first MCP item in "{field}" has "{key}" equal to {value:d}')
def step_mcp_first_item_int(context, field, key, value):
    assert context.mcp_error is None, f"MCP tool raised: {context.mcp_error}"
    items = context.mcp_result[field]
    assert items, f'Expected "{field}" to be non-empty'
    actual = items[0].get(key)
    assert actual == value, f"Expected items[0].{key}={value}, got {actual!r}"


@then("the MCP tool raises a SubstackAuthError")
def step_mcp_raises_auth_error(context):
    from gateway_oss.client.base import SubstackAuthError

    assert isinstance(context.mcp_error, SubstackAuthError), (
        f"Expected SubstackAuthError, got {type(context.mcp_error).__name__}: "
        f"{context.mcp_error}"
    )
