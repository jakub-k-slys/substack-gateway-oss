from __future__ import annotations

import os

import httpx


def before_scenario(context, scenario):
    configured_base_url = os.environ.get("SUBSTACK_GATEWAY_BASE_URL", "").strip()
    base_url = configured_base_url or "http://localhost:5001"
    timeout_sec = float(os.environ.get("SUBSTACK_GATEWAY_E2E_TIMEOUT_SEC", "120"))
    context.client = httpx.Client(
        base_url=base_url,
        timeout=httpx.Timeout(timeout_sec),
    )
    context.headers: dict[str, str] = {}
    context.response = None
    context.mcp_response = None
    context.mcp_payload = None
    context.draft_id = None
    context.draft_deleted = False

    if not configured_base_url:
        try:
            context.client.get("/")
        except httpx.HTTPError:
            scenario.skip(
                "SUBSTACK_GATEWAY_BASE_URL not configured and local gateway is not running"
            )


def after_scenario(context, scenario):
    # Best-effort cleanup so a failing scenario does not leave a draft behind.
    if context.draft_id and not context.draft_deleted:
        try:
            context.client.delete(
                f"/api/v1/drafts/{context.draft_id}", headers=context.headers
            )
        except httpx.HTTPError:
            pass
    context.client.close()
