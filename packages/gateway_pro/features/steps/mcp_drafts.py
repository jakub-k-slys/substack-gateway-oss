"""Behave step definitions for pro MCP draft tools."""

from __future__ import annotations

import asyncio

from behave import when
from gateway_oss.auth import (
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway_oss.mcp.app import (
    create_draft,
    delete_draft,
    get_draft,
    list_drafts,
)
from gateway_pro.services.drafts import DraftsService


def _call(context, coro):
    try:
        context.mcp_result = asyncio.run(coro)
        context.mcp_error = None
    except Exception as exc:  # noqa: BLE001
        context.mcp_result = None
        context.mcp_error = exc


@when("I call the MCP tool list_drafts")
def step_call_list_drafts(context):
    async def run():
        creds = decode_bearer_credentials(context.mcp_token)
        async with (
            make_publication_client(creds, context.mcp_pub_url) as pub,
            make_substack_client(creds) as sub,
        ):
            return await list_drafts(drafts=DraftsService(pub, sub))

    _call(context, run())


@when("I call the MCP tool get_draft with draft_id {draft_id:d}")
def step_call_get_draft(context, draft_id):
    async def run():
        creds = decode_bearer_credentials(context.mcp_token)
        async with (
            make_publication_client(creds, context.mcp_pub_url) as pub,
            make_substack_client(creds) as sub,
        ):
            return await get_draft(draft_id=draft_id, drafts=DraftsService(pub, sub))

    _call(context, run())


@when('I call the MCP tool create_draft with title "{title}"')
def step_call_create_draft(context, title):
    async def run():
        creds = decode_bearer_credentials(context.mcp_token)
        async with (
            make_publication_client(creds, context.mcp_pub_url) as pub,
            make_substack_client(creds) as sub,
        ):
            return await create_draft(title=title, drafts=DraftsService(pub, sub))

    _call(context, run())


@when("I call the MCP tool delete_draft with draft_id {draft_id:d}")
def step_call_delete_draft(context, draft_id):
    async def run():
        creds = decode_bearer_credentials(context.mcp_token)
        async with (
            make_publication_client(creds, context.mcp_pub_url) as pub,
            make_substack_client(creds) as sub,
        ):
            return await delete_draft(draft_id=draft_id, drafts=DraftsService(pub, sub))

    _call(context, run())
