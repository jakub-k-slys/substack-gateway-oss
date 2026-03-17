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
import contextlib
import json
from collections.abc import AsyncIterator

from behave import given, then, when

from gateway.auth import (
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway.client.publication import PublicationClient
from gateway.client.substack import SubstackClient
from gateway.mcp.app import (
    create_draft,
    create_note,
    delete_draft,
    delete_note,
    get_draft,
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
    list_drafts,
)
from gateway.services.following import FollowingService
from gateway.services.notes import NotesService
from gateway.services.posts import PostsService
from gateway.services.profiles import ProfilesService
from gateway_pro.services.drafts import DraftsService

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


@contextlib.asynccontextmanager
async def _clients(
    context,
) -> AsyncIterator[tuple[PublicationClient, SubstackClient]]:
    """Create and enter authenticated pub + sub clients from test context."""
    creds = decode_bearer_credentials(context.mcp_token)
    async with (
        make_publication_client(creds, context.mcp_pub_url) as pub,
        make_substack_client(creds) as sub,
    ):
        yield pub, sub


# ------------------------------------------------------------------
# When — notes
# ------------------------------------------------------------------


@when("I call the MCP tool get_note with note_id {note_id:d}")
def step_call_get_note(context, note_id):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_note(note_id=note_id, notes=NotesService(pub, sub))

    _call(context, run())


@when('I call the MCP tool create_note with content "{content}"')
def step_call_create_note(context, content):
    async def run():
        async with _clients(context) as (pub, sub):
            return await create_note(content=content, notes=NotesService(pub, sub))

    _call(context, run())


@when("I call the MCP tool delete_note with note_id {note_id:d}")
def step_call_delete_note(context, note_id):
    async def run():
        async with _clients(context) as (pub, sub):
            return await delete_note(note_id=note_id, notes=NotesService(pub, sub))

    _call(context, run())


# ------------------------------------------------------------------
# When — drafts
# ------------------------------------------------------------------


@when("I call the MCP tool list_drafts")
def step_call_list_drafts(context):
    async def run():
        async with _clients(context) as (pub, sub):
            return await list_drafts(drafts=DraftsService(pub, sub))

    _call(context, run())


@when("I call the MCP tool get_draft with draft_id {draft_id:d}")
def step_call_get_draft(context, draft_id):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_draft(draft_id=draft_id, drafts=DraftsService(pub, sub))

    _call(context, run())


@when('I call the MCP tool create_draft with title "{title}"')
def step_call_create_draft(context, title):
    async def run():
        async with _clients(context) as (pub, sub):
            return await create_draft(title=title, drafts=DraftsService(pub, sub))

    _call(context, run())


@when("I call the MCP tool delete_draft with draft_id {draft_id:d}")
def step_call_delete_draft(context, draft_id):
    async def run():
        async with _clients(context) as (pub, sub):
            return await delete_draft(draft_id=draft_id, drafts=DraftsService(pub, sub))

    _call(context, run())


# ------------------------------------------------------------------
# When — me / posts
# ------------------------------------------------------------------


@when("I call the MCP tool get_me")
def step_call_get_me(context):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_me(profiles=ProfilesService(sub))

    _call(context, run())


@when("I call the MCP tool get_my_notes")
def step_call_get_my_notes(context):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_my_notes(notes=NotesService(pub, sub))

    _call(context, run())


@when("I call the MCP tool get_my_posts")
def step_call_get_my_posts(context):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_my_posts(
                profiles=ProfilesService(sub), posts=PostsService(pub, sub)
            )

    _call(context, run())


@when("I call the MCP tool get_post with post_id {post_id:d}")
def step_call_get_post(context, post_id):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_post(post_id=post_id, posts=PostsService(pub, sub))

    _call(context, run())


@when("I call the MCP tool get_post_comments with post_id {post_id:d}")
def step_call_get_post_comments(context, post_id):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_post_comments(
                post_id=post_id, posts=PostsService(pub, sub)
            )

    _call(context, run())


@when("I call the MCP tool get_my_following")
def step_call_get_my_following(context):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_my_following(following=FollowingService(pub, sub))

    _call(context, run())


# ------------------------------------------------------------------
# When — profiles
# ------------------------------------------------------------------


@when('I call the MCP tool get_profile with slug "{slug}"')
def step_call_get_profile(context, slug):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_profile(slug=slug, profiles=ProfilesService(sub))

    _call(context, run())


@when('I call the MCP tool get_profile_posts with slug "{slug}"')
def step_call_get_profile_posts(context, slug):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_profile_posts(
                slug=slug,
                profiles=ProfilesService(sub),
                posts=PostsService(pub, sub),
            )

    _call(context, run())


@when('I call the MCP tool get_profile_notes with slug "{slug}"')
def step_call_get_profile_notes(context, slug):
    async def run():
        async with _clients(context) as (pub, sub):
            return await get_profile_notes(
                slug=slug,
                profiles=ProfilesService(sub),
                posts=PostsService(pub, sub),
            )

    _call(context, run())


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
