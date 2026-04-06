"""Behave step definitions for pro MCP draft tools."""

from __future__ import annotations

import asyncio

from behave import when
from gateway_pro.mcp.app import (
    create_draft,
    delete_draft,
    get_draft,
    like_note,
    list_drafts,
    unlike_note,
)


def _call(context, coro):
    try:
        context.mcp_result = asyncio.run(coro)
        context.mcp_error = None
    except Exception as exc:  # noqa: BLE001
        context.mcp_result = None
        context.mcp_error = exc


@when("I call the MCP tool list_drafts")
def step_call_list_drafts(context):
    _call(context, list_drafts(token=context.mcp_token))


@when("I call the MCP tool get_draft with draft_id {draft_id:d}")
def step_call_get_draft(context, draft_id):
    _call(context, get_draft(draft_id=draft_id, token=context.mcp_token))


@when('I call the MCP tool create_draft with title "{title}"')
def step_call_create_draft(context, title):
    _call(context, create_draft(title=title, token=context.mcp_token))


@when("I call the MCP tool delete_draft with draft_id {draft_id:d}")
def step_call_delete_draft(context, draft_id):
    _call(context, delete_draft(draft_id=draft_id, token=context.mcp_token))


@when("I call the MCP tool like_note with note_id {note_id:d}")
def step_call_like_note(context, note_id):
    _call(context, like_note(note_id=note_id, token=context.mcp_token))


@when("I call the MCP tool unlike_note with note_id {note_id:d}")
def step_call_unlike_note(context, note_id):
    _call(context, unlike_note(note_id=note_id, token=context.mcp_token))
