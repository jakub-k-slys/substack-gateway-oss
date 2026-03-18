from __future__ import annotations

import httpx
from behave import given

from common_shim import SUBSTACK_BASE, load_sample


def _draft_url(context, draft_id: int | None = None) -> str:
    pub = context.headers.get("x-publication-url")
    if not pub:
        raise RuntimeError("x-publication-url not set — missing a Given step?")
    base = f"{pub.rstrip('/')}/api/v1/drafts"
    return f"{base}/{draft_id}" if draft_id is not None else base


def _create_draft_url(context) -> str:
    return _draft_url(context)


def _user_settings_url() -> str:
    return f"{SUBSTACK_BASE}/api/v1/user-settings"


_USER_SETTINGS_RESPONSE = {
    "userSettings": [
        {
            "user_id": 254824415,
            "type": "last_home_tab",
            "value_bool": None,
            "value_datetime": None,
            "value_integer": None,
            "value_text": "inbox",
        }
    ],
    "qualifiesForBadge": False,
}


@given(
    "the Substack get-draft endpoint returns the sample response for draft {draft_id:d}"
)
def step_get_draft_returns_sample(context, draft_id):
    context.respx_mock.get(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(200, json=load_sample("api/v1/draft/get-response"))
    )


@given(
    "the Substack get-draft endpoint returns status {status:d} for draft {draft_id:d}"
)
def step_get_draft_returns_status(context, status, draft_id):
    context.respx_mock.get(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(status)
    )


@given(
    "the Substack update-draft endpoint returns the sample response for draft {draft_id:d}"
)
def step_update_draft_returns_sample(context, draft_id):
    context.respx_mock.put(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(200, json=load_sample("api/v1/draft/get-response"))
    )


@given(
    "the Substack update-draft endpoint returns status {status:d} for draft {draft_id:d}"
)
def step_update_draft_returns_status(context, status, draft_id):
    context.respx_mock.put(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(status)
    )


@given(
    "the Substack delete-draft endpoint returns status {status:d} for draft {draft_id:d}"
)
def step_delete_draft_returns_status(context, status, draft_id):
    context.respx_mock.delete(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(status)
    )


@given("the Substack list-drafts endpoint returns the sample response")
def step_list_drafts_returns_sample(context):
    context.respx_mock.get(_draft_url(context)).mock(
        return_value=httpx.Response(
            200, json=load_sample("api/v1/drafts/list-response")
        )
    )


@given("the Substack list-drafts endpoint returns status {status:d}")
def step_list_drafts_returns_status(context, status):
    context.respx_mock.get(_draft_url(context)).mock(
        return_value=httpx.Response(status)
    )


@given("the Substack create-draft endpoint returns the sample response")
def step_create_draft_returns_sample(context):
    context.respx_mock.get(_user_settings_url()).mock(
        return_value=httpx.Response(200, json=_USER_SETTINGS_RESPONSE)
    )
    context.respx_mock.post(_create_draft_url(context)).mock(
        return_value=httpx.Response(201, json=load_sample("api/v1/draft/response"))
    )


@given("the Substack create-draft endpoint returns status {status:d}")
def step_create_draft_returns_status(context, status):
    context.respx_mock.get(_user_settings_url()).mock(
        return_value=httpx.Response(200, json=_USER_SETTINGS_RESPONSE)
    )
    context.respx_mock.post(_create_draft_url(context)).mock(
        return_value=httpx.Response(status)
    )
