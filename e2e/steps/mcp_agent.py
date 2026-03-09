"""Step definitions for MCP agent flow e2e tests.

Simulates a full MCP agent lifecycle: OAuth discovery → client registration →
authorization → token exchange → MCP initialize → tool calls, all using raw
HTTP against the gateway's streamable-http MCP transport.

A temporary test user is created via POST /api/v1/users before each scenario
and deleted via DELETE /api/v1/users afterward — no pre-existing user needed.

Required environment variables:
  SUBSTACK_TOKEN           — base64-encoded Substack credentials
  SUBSTACK_PUBLICATION_URL — publication URL (e.g. https://example.substack.com)

  SUBSTACK_GATEWAY_ADMIN_TOKEN — admin token for user management API
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import urllib.parse
from base64 import urlsafe_b64encode

from behave import given, then, when

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_MCP_REQUEST_ID = 0


def _next_id() -> int:
    global _MCP_REQUEST_ID
    _MCP_REQUEST_ID += 1
    return _MCP_REQUEST_ID


def _mcp_headers(access_token: str | None = None) -> dict[str, str]:
    """Build MCP streamable-http request headers."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    return headers


def _mcp_request(method: str, params: dict | None = None) -> dict:
    """Build a JSON-RPC 2.0 request."""
    msg: dict = {
        "jsonrpc": "2.0",
        "id": _next_id(),
        "method": method,
    }
    if params is not None:
        msg["params"] = params
    return msg


def _parse_mcp_response(response) -> dict:
    """Parse an MCP response — handles both JSON and SSE responses."""
    content_type = response.headers.get("content-type", "").lower()
    if "text/event-stream" in content_type:
        # Parse SSE: look for 'data:' lines containing JSON-RPC messages
        for line in response.text.splitlines():
            if line.startswith("data:") and line.strip() != "data:":
                data = line[len("data:") :].strip()
                if data:
                    return json.loads(data)
        raise ValueError(f"No JSON-RPC message found in SSE response: {response.text}")
    return response.json()


def _generate_pkce() -> tuple[str, str]:
    """Generate PKCE code_verifier and code_challenge (S256)."""
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return verifier, challenge


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------


@given("OAuth is enabled on the gateway")
def step_oauth_enabled(context):
    token = os.environ.get("SUBSTACK_TOKEN", "")
    pub_url = os.environ.get("SUBSTACK_PUBLICATION_URL", "")
    admin_token = os.environ.get("SUBSTACK_GATEWAY_ADMIN_TOKEN", "")
    if not all([token, pub_url, admin_token]):
        context.scenario.skip(
            "SUBSTACK_TOKEN, SUBSTACK_PUBLICATION_URL, and "
            "SUBSTACK_GATEWAY_ADMIN_TOKEN are all required "
            "for MCP agent flow tests"
        )
        return
    context.substack_token = token
    context.publication_url = pub_url
    context.admin_token = admin_token
    context.pkce_verifier, context.pkce_challenge = _generate_pkce()
    context.oauth_state = secrets.token_urlsafe(32)
    context.redirect_uri = "http://localhost:19876/callback"


@given("a temporary test user exists")
def step_create_temp_user(context):
    # Fixed, clearly-test-only email — never collides with real users.
    # Only the password is randomised (so concurrent runs don't share state).
    context.oauth_email = "e2e-mcp-agent-test@test.gateway.local"
    context.oauth_password = secrets.token_urlsafe(24)

    # Delete any leftover from a previous failed run before creating
    context.client.request(
        "DELETE",
        "/api/v1/users",
        params={"token": context.admin_token},
        json={"email": context.oauth_email},
    )

    resp = context.client.post(
        "/api/v1/users",
        params={"token": context.admin_token},
        json={
            "email": context.oauth_email,
            "password": context.oauth_password,
        },
    )
    assert resp.status_code == 201, (
        f"Failed to create test user: {resp.status_code} {resp.text}"
    )

    # Register cleanup so the user is deleted after the scenario
    context.add_cleanup(_delete_temp_user, context)


def _delete_temp_user(context):
    """Cleanup callback — delete the temporary test user after the scenario."""
    try:
        context.client.request(
            "DELETE",
            "/api/v1/users",
            params={"token": context.admin_token},
            json={"email": context.oauth_email},
        )
    except Exception:
        pass  # Best-effort cleanup


# ---------------------------------------------------------------------------
# When — OAuth discovery and registration
# ---------------------------------------------------------------------------


@when("I discover the OAuth metadata")
def step_discover_metadata(context):
    # Try path-aware discovery first (RFC 8414), then fall back
    resp = context.client.get("/.well-known/oauth-authorization-server/mcp")
    if resp.status_code == 404:
        resp = context.client.get("/.well-known/oauth-authorization-server")
    assert resp.status_code == 200, (
        f"OAuth metadata discovery failed: {resp.status_code} {resp.text}"
    )
    context.oauth_metadata = resp.json()


@when("I register as an OAuth client via the registration endpoint")
def step_register_client(context):
    reg_url = context.oauth_metadata.get("registration_endpoint", "")
    assert reg_url, "No registration_endpoint in OAuth metadata"

    # Use the path portion of the registration URL
    parsed = urllib.parse.urlparse(reg_url)
    resp = context.client.post(
        parsed.path,
        json={
            "client_name": "e2e-mcp-agent-test",
            "redirect_uris": [context.redirect_uri],
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
            "token_endpoint_auth_method": "client_secret_post",
        },
    )
    assert resp.status_code in (200, 201), (
        f"Client registration failed: {resp.status_code} {resp.text}"
    )
    data = resp.json()
    context.client_id = data["client_id"]
    context.client_secret = data.get("client_secret")


@when("I start the OAuth authorization flow")
def step_start_authorization(context):
    auth_url = context.oauth_metadata.get("authorization_endpoint", "")
    assert auth_url, "No authorization_endpoint in OAuth metadata"

    parsed = urllib.parse.urlparse(auth_url)
    params = {
        "response_type": "code",
        "client_id": context.client_id,
        "redirect_uri": context.redirect_uri,
        "state": context.oauth_state,
        "code_challenge": context.pkce_challenge,
        "code_challenge_method": "S256",
    }
    resp = context.client.get(parsed.path, params=params, follow_redirects=False)
    # Should redirect to login page
    assert resp.status_code in (302, 303, 307), (
        f"Expected redirect, got {resp.status_code}: {resp.text}"
    )
    context.login_redirect = resp.headers.get("location", "")


@when("I complete the login and token submission")
def step_complete_login(context):
    # Phase 1: Extract request_id from login redirect URL
    parsed = urllib.parse.urlparse(context.login_redirect)
    qs = urllib.parse.parse_qs(parsed.query)
    request_id = qs.get("request_id", [""])[0]
    assert request_id, f"No request_id in login redirect: {context.login_redirect}"

    # Phase 1: POST email + password
    login_path = parsed.path or "/login"
    resp = context.client.post(
        f"{login_path}/",
        data={
            "request_id": request_id,
            "email": context.oauth_email,
            "password": context.oauth_password,
        },
        follow_redirects=False,
    )
    assert resp.status_code == 302, (
        f"Login phase 1 failed: {resp.status_code} {resp.text}"
    )

    # Extract session_id from redirect
    location = resp.headers.get("location", "")
    session_id_match = re.search(r"session_id=([^&]+)", location)
    assert session_id_match, f"No session_id in redirect: {location}"
    session_id = session_id_match.group(1)

    # Phase 2: POST Substack token + publication URL
    resp = context.client.post(
        "/login/token/",
        data={
            "session_id": session_id,
            "token": context.substack_token,
            "pub_url": context.publication_url,
        },
    )
    assert resp.status_code == 200, (
        f"Token submission failed: {resp.status_code} {resp.text}"
    )

    # Extract authorization code from the success page redirect URL
    # The success page contains a JS redirect or a link with the callback URL
    code_match = re.search(r"code=([^&\"']+)", resp.text)
    assert code_match, f"No authorization code in success response: {resp.text[:500]}"
    context.auth_code = code_match.group(1)

    # Extract state to verify it matches
    state_match = re.search(r"state=([^&\"']+)", resp.text)
    if state_match:
        returned_state = urllib.parse.unquote(state_match.group(1))
        assert returned_state == context.oauth_state, (
            f"State mismatch: expected {context.oauth_state}, got {returned_state}"
        )


@when("I exchange the authorization code for tokens")
def step_exchange_code(context):
    token_url = context.oauth_metadata.get("token_endpoint", "")
    assert token_url, "No token_endpoint in OAuth metadata"

    parsed = urllib.parse.urlparse(token_url)
    data = {
        "grant_type": "authorization_code",
        "code": context.auth_code,
        "redirect_uri": context.redirect_uri,
        "client_id": context.client_id,
        "code_verifier": context.pkce_verifier,
    }
    if context.client_secret:
        data["client_secret"] = context.client_secret

    resp = context.client.post(
        parsed.path,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200, (
        f"Token exchange failed: {resp.status_code} {resp.text}"
    )
    token_data = resp.json()
    context.access_token = token_data["access_token"]
    context.refresh_token = token_data.get("refresh_token")
    context.token_type = token_data.get("token_type", "Bearer")


@when("I save the current tokens")
def step_save_tokens(context):
    context.original_access_token = context.access_token
    context.original_refresh_token = context.refresh_token


@when("I exchange the refresh token for new tokens")
def step_refresh_token(context):
    token_url = context.oauth_metadata.get("token_endpoint", "")
    parsed = urllib.parse.urlparse(token_url)
    data = {
        "grant_type": "refresh_token",
        "refresh_token": context.refresh_token,
        "client_id": context.client_id,
    }
    if context.client_secret:
        data["client_secret"] = context.client_secret

    resp = context.client.post(
        parsed.path,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200, (
        f"Token refresh failed: {resp.status_code} {resp.text}"
    )
    token_data = resp.json()
    context.refreshed_access_token = token_data["access_token"]
    context.refresh_token = token_data.get("refresh_token", context.refresh_token)
    # Update the current access token for subsequent requests
    context.access_token = context.refreshed_access_token


# ---------------------------------------------------------------------------
# When — MCP protocol (JSON-RPC over streamable-http)
# ---------------------------------------------------------------------------


@when("I send an MCP initialize request with the access token")
def step_mcp_initialize(context):
    _do_mcp_initialize(context, context.access_token)


@when("I send an MCP initialize request with the refreshed access token")
def step_mcp_initialize_refreshed(context):
    _do_mcp_initialize(context, context.refreshed_access_token)


@when("I send an MCP initialize request with the original access token")
def step_mcp_initialize_original(context):
    _do_mcp_initialize(context, context.original_access_token)


def _do_mcp_initialize(context, token: str):
    payload = _mcp_request(
        "initialize",
        {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "e2e-test-agent", "version": "1.0.0"},
        },
    )
    resp = context.client.post(
        "/mcp/",
        json=payload,
        headers=_mcp_headers(token),
    )
    context.mcp_init_response = resp
    context.mcp_init_status = resp.status_code
    if resp.status_code == 200:
        context.mcp_init_data = _parse_mcp_response(resp)
        # Store session ID if present
        session_id = resp.headers.get("mcp-session-id")
        if session_id:
            context.mcp_session_id = session_id
        # Send initialized notification
        notif = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
        }
        headers = _mcp_headers(token)
        if hasattr(context, "mcp_session_id"):
            headers["mcp-session-id"] = context.mcp_session_id
        context.client.post("/mcp/", json=notif, headers=headers)
        context.mcp_current_token = token


@when("I send an MCP tools/list request")
def step_mcp_tools_list(context):
    payload = _mcp_request("tools/list", {})
    headers = _mcp_headers(context.mcp_current_token)
    if hasattr(context, "mcp_session_id"):
        headers["mcp-session-id"] = context.mcp_session_id
    resp = context.client.post("/mcp/", json=payload, headers=headers)
    assert resp.status_code == 200, f"tools/list failed: {resp.status_code} {resp.text}"
    context.mcp_tools_response = _parse_mcp_response(resp)


@when('I call the MCP tool "{tool_name}" with no arguments')
def step_mcp_call_tool(context, tool_name):
    payload = _mcp_request(
        "tools/call",
        {
            "name": tool_name,
            "arguments": {},
        },
    )
    headers = _mcp_headers(context.mcp_current_token)
    if hasattr(context, "mcp_session_id"):
        headers["mcp-session-id"] = context.mcp_session_id
    resp = context.client.post("/mcp/", json=payload, headers=headers)
    context.mcp_tool_call_status = resp.status_code
    if resp.status_code == 200:
        context.mcp_tool_call_response = _parse_mcp_response(resp)
    else:
        context.mcp_tool_call_response = None


# ---------------------------------------------------------------------------
# Then — OAuth assertions
# ---------------------------------------------------------------------------


@then("the metadata contains token and authorization endpoints")
def step_metadata_has_endpoints(context):
    md = context.oauth_metadata
    assert "token_endpoint" in md, f"Missing token_endpoint. Keys: {list(md.keys())}"
    assert "authorization_endpoint" in md, (
        f"Missing authorization_endpoint. Keys: {list(md.keys())}"
    )


@then("I have a registered client_id")
def step_has_client_id(context):
    assert context.client_id, "client_id is empty"


@then("I am redirected to the login page")
def step_redirected_to_login(context):
    assert "login" in context.login_redirect.lower(), (
        f"Expected redirect to login page, got: {context.login_redirect}"
    )


@then("I have an authorization code")
def step_has_auth_code(context):
    assert context.auth_code, "Authorization code is empty"


@then("I have an access token and a refresh token")
def step_has_tokens(context):
    assert context.access_token, "Access token is empty"
    assert context.refresh_token, "Refresh token is empty"


@then("the new access token differs from the original")
def step_new_token_differs(context):
    assert context.refreshed_access_token != context.original_access_token, (
        "Refreshed access token should differ from the original"
    )


# ---------------------------------------------------------------------------
# Then — MCP assertions
# ---------------------------------------------------------------------------


@then("the MCP server responds with capabilities")
def step_mcp_has_capabilities(context):
    assert context.mcp_init_status == 200, (
        f"MCP initialize failed with {context.mcp_init_status}: "
        f"{context.mcp_init_response.text}"
    )
    data = context.mcp_init_data
    result = data.get("result", {})
    assert "capabilities" in result, f"No capabilities in MCP init response: {data}"


@then('the tool list includes "{tool_name}"')
def step_tool_list_includes(context, tool_name):
    result = context.mcp_tools_response.get("result", {})
    tools = result.get("tools", [])
    tool_names = [t.get("name") for t in tools]
    assert tool_name in tool_names, (
        f'Expected "{tool_name}" in tool list, got: {tool_names}'
    )


@then("the MCP tool call succeeds")
def step_tool_call_succeeds(context):
    assert context.mcp_tool_call_status == 200, (
        f"Tool call failed with status {context.mcp_tool_call_status}"
    )
    data = context.mcp_tool_call_response
    assert data is not None, "No response data from tool call"
    # JSON-RPC success has "result", error has "error"
    assert "error" not in data, f"Tool call returned error: {data.get('error')}"
    assert "result" in data, f"Tool call missing result: {data}"


@then("the MCP server rejects the request")
def step_mcp_rejects(context):
    # Revoked token should get 401 or the MCP response should contain an error
    assert context.mcp_init_status in (401, 403), (
        f"Expected 401/403 for revoked token, got {context.mcp_init_status}"
    )
