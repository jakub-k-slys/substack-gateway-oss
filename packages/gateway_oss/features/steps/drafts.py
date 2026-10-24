from __future__ import annotations

import asyncio
import json

import httpx
from pytest_bdd import given, parsers, then, when

from gateway_drafts_mcp.tools import create_draft, get_draft, update_draft

from .common import SUBSTACK_BASE, load_sample, pub_url

_RICH_SAMPLE = "api/v1/draft/get-rich-response"


def _draft_url(context, draft_id: int | None = None) -> str:
    pub = pub_url(context)
    if not pub:
        raise RuntimeError("publication URL not set — missing a Given step?")
    base = f"{pub}/api/v1/drafts"
    return f"{base}/{draft_id}" if draft_id is not None else base


def _list_drafts_url(context) -> str:
    pub = pub_url(context)
    if not pub:
        raise RuntimeError("publication URL not set — missing a Given step?")
    return f"{pub}/api/v1/post_management/drafts"


def _create_draft_url(context) -> str:
    return _draft_url(context)


def _watermark_url(context) -> str:
    return f"{pub_url(context)}/api/v1/image/watermark"


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
    parsers.parse(
        "the Substack get-draft endpoint returns the sample response for draft {draft_id:d}"
    )
)
def step_get_draft_returns_sample(context, draft_id):
    context.respx_mock.get(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(200, json=load_sample("api/v1/draft/get-response"))
    )


@given(
    parsers.parse(
        "the Substack get-draft endpoint returns the rich sample for draft {draft_id:d}"
    )
)
def step_get_draft_returns_rich_sample(context, draft_id):
    context.respx_mock.get(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(200, json=load_sample(_RICH_SAMPLE))
    )


@given(
    parsers.parse(
        "the Substack get-draft endpoint returns status {status:d} for draft {draft_id:d}"
    )
)
def step_get_draft_returns_status(context, status, draft_id):
    context.respx_mock.get(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(status)
    )


@given(
    parsers.parse(
        "the Substack update-draft endpoint returns the sample response for draft {draft_id:d}"
    )
)
def step_update_draft_returns_sample(context, draft_id):
    context.respx_mock.put(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(200, json=load_sample("api/v1/draft/get-response"))
    )


@given(
    parsers.parse(
        "the Substack update-draft endpoint returns status {status:d} for draft {draft_id:d}"
    )
)
def step_update_draft_returns_status(context, status, draft_id):
    context.respx_mock.put(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(status)
    )


@given(
    parsers.parse(
        "the Substack delete-draft endpoint returns status {status:d} for draft {draft_id:d}"
    )
)
def step_delete_draft_returns_status(context, status, draft_id):
    context.respx_mock.delete(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(status)
    )


@given(parsers.parse('the Substack watermark endpoint returns "{url}"'))
def step_watermark_returns_url(context, url):
    context.respx_mock.post(_watermark_url(context)).mock(
        return_value=httpx.Response(200, json={"url": url})
    )


@given("the Substack list-drafts endpoint returns the sample response")
def step_list_drafts_returns_sample(context):
    context.respx_mock.get(_list_drafts_url(context)).mock(
        return_value=httpx.Response(
            200, json=load_sample("api/v1/drafts/list-response")
        )
    )


@given(parsers.parse("the Substack list-drafts endpoint returns status {status:d}"))
def step_list_drafts_returns_status(context, status):
    context.respx_mock.get(_list_drafts_url(context)).mock(
        return_value=httpx.Response(status)
    )


@given("the Substack user-settings endpoint returns the sample response")
def step_user_settings_returns_sample(context):
    context.respx_mock.get(_user_settings_url()).mock(
        return_value=httpx.Response(200, json=_USER_SETTINGS_RESPONSE)
    )


@given("the Substack create-draft endpoint returns the sample response")
def step_create_draft_returns_sample(context):
    context.respx_mock.get(_user_settings_url()).mock(
        return_value=httpx.Response(200, json=_USER_SETTINGS_RESPONSE)
    )
    context.respx_mock.post(_create_draft_url(context)).mock(
        return_value=httpx.Response(201, json=load_sample("api/v1/draft/response"))
    )


@given(parsers.parse("the Substack create-draft endpoint returns status {status:d}"))
def step_create_draft_returns_status(context, status):
    context.respx_mock.get(_user_settings_url()).mock(
        return_value=httpx.Response(200, json=_USER_SETTINGS_RESPONSE)
    )
    context.respx_mock.post(_create_draft_url(context)).mock(
        return_value=httpx.Response(status)
    )


def _upstream_calls(context, method: str, url: str) -> list:
    return [
        call
        for call in context.respx_mock.calls
        if call.request.method == method and str(call.request.url) == url
    ]


@then("no Substack PUT request was sent")
def step_no_substack_put(context):
    puts = [c for c in context.respx_mock.calls if c.request.method == "PUT"]
    assert not puts, f"Expected no upstream PUT, got {len(puts)}"


@then("no Substack POST request was sent to the drafts endpoint")
def step_no_substack_draft_post(context):
    posts = _upstream_calls(context, "POST", _create_draft_url(context))
    assert not posts, f"Expected no upstream draft POST, got {len(posts)}"


def _canonical(draft_body: str) -> str:
    return json.dumps(json.loads(draft_body), sort_keys=True)


def _single_upstream_json(context, method: str, url: str) -> dict:
    calls = _upstream_calls(context, method, url)
    assert len(calls) == 1, f"Expected one upstream {method} to {url}, got {len(calls)}"
    return json.loads(calls[0].request.content)


@when(
    parsers.parse(
        "I send PUT /api/v1/drafts/{draft_id:d} with the body and updated_at "
        "from the previous response"
    )
)
def step_put_fetched_body(context, draft_id):
    fetched = context.response.json()
    assert context.response.status_code == 200, context.response.text
    context.response = context.client.put(
        f"/api/v1/drafts/{draft_id}",
        json={
            "body": fetched["body"],
            "expected_updated_at": fetched["updated_at"],
        },
        headers=context.headers,
    )


@when(
    parsers.parse(
        "I call the MCP tool get_draft then update_draft with draft_id {draft_id:d}"
    )
)
def step_mcp_get_then_update(context, draft_id):
    async def round_trip():
        fetched = await get_draft(draft_id=draft_id, token=context.mcp_token)
        return await update_draft(
            draft_id=draft_id,
            body=fetched["body"],
            expected_updated_at=fetched["updated_at"],
            token=context.mcp_token,
        )

    try:
        context.mcp_result = asyncio.run(round_trip())
        context.mcp_error = None
    except Exception as exc:  # noqa: BLE001
        context.mcp_result = None
        context.mcp_error = exc


@when(parsers.parse('I call the MCP tool create_draft with body "{body}"'))
def step_mcp_create_draft_with_body(context, body):
    try:
        context.mcp_result = asyncio.run(
            create_draft(title="Test Draft", body=body, token=context.mcp_token)
        )
        context.mcp_error = None
    except Exception as exc:  # noqa: BLE001
        context.mcp_result = None
        context.mcp_error = exc


@then("the upstream draft PUT body equals the rich sample draft_body")
def step_upstream_put_equals_rich_sample(context):
    sent = _single_upstream_json(context, "PUT", _draft_url(context, 189535264))
    expected = load_sample(_RICH_SAMPLE)["draft_body"]
    assert _canonical(sent["draft_body"]) == _canonical(expected), (
        "Upstream draft_body differs from the rich sample:\n"
        f"sent:     {_canonical(sent['draft_body'])}\n"
        f"expected: {_canonical(expected)}"
    )


@then(
    parsers.parse(
        "the upstream watermark request has offsetX {x:d} offsetY {y:d} width {w:d}"
    )
)
def step_upstream_watermark_geometry(context, x, y, w):
    body = _single_upstream_json(context, "POST", _watermark_url(context))
    actual = (body["offsetX"], body["offsetY"], body["width"], body["height"])
    assert actual == (x, y, w, w), f"Expected {(x, y, w, w)}, got {actual}"


@then(
    parsers.parse(
        'the upstream watermark request is for image "{url}" with opacity {opacity:d}'
    )
)
def step_upstream_watermark_image(context, url, opacity):
    body = _single_upstream_json(context, "POST", _watermark_url(context))
    assert body["image"] == url, f"Expected image {url}, got {body['image']}"
    assert body["opacity"] == opacity, f"Expected opacity {opacity}, got {body}"


def _created_images(context) -> list[dict]:
    sent = _single_upstream_json(context, "POST", _create_draft_url(context))
    found: list[dict] = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "image2":
                found.append(node["attrs"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(json.loads(sent["draft_body"]))
    return found


@then(
    parsers.parse(
        'the created draft has one image with src "{src}" and srcNoWatermark "{original}"'
    )
)
def step_created_image_watermarked(context, src, original):
    images = _created_images(context)
    assert len(images) == 1, f"Expected one image2 node, got {len(images)}"
    attrs = images[0]
    assert attrs["src"] == src, f"Expected src {src}, got {attrs['src']}"
    assert attrs["srcNoWatermark"] == original, (
        f"Expected srcNoWatermark {original}, got {attrs['srcNoWatermark']}"
    )
