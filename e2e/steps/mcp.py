from __future__ import annotations

import json
import os

from behave import then, when


def _e2e_token() -> str:
    return (
        os.environ.get("SUBSTACK_GATEWAY_TOKEN", "").strip()
        or os.environ.get("SUBSTACK_TOKEN", "").strip()
    )


def _mcp_headers(session_id: str | None = None) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["mcp-session-id"] = session_id
    return headers


def _mcp_request(method: str, request_id: int, params: dict | None = None) -> dict:
    payload: dict[str, object] = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
    }
    if params is not None:
        payload["params"] = params
    return payload


def _parse_mcp_response(response) -> dict:
    content_type = response.headers.get("content-type", "").lower()
    if "text/event-stream" in content_type:
        for line in response.text.splitlines():
            if line.startswith("data:") and line.strip() != "data:":
                return json.loads(line[len("data:") :].strip())
        raise AssertionError(
            f"No JSON-RPC message found in SSE response: {response.text}"
        )
    return response.json()


@when("I initialize the MCP session")
def step_initialize_mcp(context):
    payload = _mcp_request(
        "initialize",
        1,
        {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "gateway-oss-e2e", "version": "1.0.0"},
        },
    )
    response = context.client.post("/mcp/", json=payload, headers=_mcp_headers())
    context.mcp_response = response
    context.mcp_payload = _parse_mcp_response(response)
    context.mcp_session_id = response.headers.get("mcp-session-id")

    notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
    }
    context.client.post(
        "/mcp/",
        json=notification,
        headers=_mcp_headers(context.mcp_session_id),
    )


@when("I request the MCP tool list")
def step_mcp_tools_list(context):
    payload = _mcp_request("tools/list", 2, {})
    response = context.client.post(
        "/mcp/",
        json=payload,
        headers=_mcp_headers(getattr(context, "mcp_session_id", None)),
    )
    context.mcp_response = response
    context.mcp_payload = _parse_mcp_response(response)


@when("I call the MCP tool get_profile for the test slug")
def step_call_get_profile(context):
    payload = _mcp_request(
        "tools/call",
        3,
        {"name": "get_profile", "arguments": {"slug": context.profile_slug}},
    )
    response = context.client.post(
        "/mcp/",
        json=payload,
        headers=_mcp_headers(getattr(context, "mcp_session_id", None)),
    )
    context.mcp_response = response
    context.mcp_payload = _parse_mcp_response(response)


@when("I call the MCP tool get_post for the test post")
def step_call_get_post(context):
    payload = _mcp_request(
        "tools/call",
        4,
        {
            "name": "get_post",
            "arguments": {"post_id": int(context.post_id), "token": _e2e_token()},
        },
    )
    response = context.client.post(
        "/mcp/",
        json=payload,
        headers=_mcp_headers(getattr(context, "mcp_session_id", None)),
    )
    context.mcp_response = response
    context.mcp_payload = _parse_mcp_response(response)


@when("I call the MCP tool get_post_comments for the test post")
def step_call_get_post_comments(context):
    payload = _mcp_request(
        "tools/call",
        6,
        {
            "name": "get_post_comments",
            "arguments": {"post_id": int(context.post_id), "token": _e2e_token()},
        },
    )
    response = context.client.post(
        "/mcp/",
        json=payload,
        headers=_mcp_headers(getattr(context, "mcp_session_id", None)),
    )
    context.mcp_response = response
    context.mcp_payload = _parse_mcp_response(response)


@when("I call the MCP tool get_note for the test note")
def step_call_get_note(context):
    payload = _mcp_request(
        "tools/call",
        5,
        {
            "name": "get_note",
            "arguments": {"note_id": int(context.note_id), "token": _e2e_token()},
        },
    )
    response = context.client.post(
        "/mcp/",
        json=payload,
        headers=_mcp_headers(getattr(context, "mcp_session_id", None)),
    )
    context.mcp_response = response
    context.mcp_payload = _parse_mcp_response(response)


@then("the MCP initialize request succeeds")
def step_mcp_initialize_succeeds(context):
    assert context.mcp_response.status_code == 200, (
        f"Expected 200, got {context.mcp_response.status_code}: {context.mcp_response.text}"
    )
    result = context.mcp_payload.get("result", {})
    assert "capabilities" in result, (
        f"No capabilities in MCP init response: {context.mcp_payload}"
    )


@then('the MCP tool list includes "{tool_name}"')
def step_mcp_tool_list_includes(context, tool_name):
    assert context.mcp_response.status_code == 200, (
        f"Expected 200, got {context.mcp_response.status_code}: {context.mcp_response.text}"
    )
    tools = context.mcp_payload.get("result", {}).get("tools", [])
    names = [tool.get("name") for tool in tools]
    assert tool_name in names, f'Expected tool "{tool_name}" in {names}'


@then("the MCP tool call succeeds")
def step_mcp_tool_call_succeeds(context):
    assert context.mcp_response.status_code == 200, (
        f"Expected 200, got {context.mcp_response.status_code}: {context.mcp_response.text}"
    )
    assert "error" not in context.mcp_payload, (
        f"MCP tool returned error: {context.mcp_payload.get('error')}"
    )
    result = context.mcp_payload.get("result")
    assert result is not None, f"MCP tool call missing result: {context.mcp_payload}"

    has_structured = (
        isinstance(result, dict) and result.get("structuredContent") is not None
    )
    has_content = isinstance(result, dict) and bool(result.get("content"))
    assert has_structured or has_content, (
        f"Expected structuredContent or content in MCP result: {context.mcp_payload}"
    )
