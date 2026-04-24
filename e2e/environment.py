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

    if not configured_base_url:
        try:
            context.client.get("/")
        except httpx.HTTPError:
            scenario.skip(
                "SUBSTACK_GATEWAY_BASE_URL not configured and local gateway is not running"
            )


def after_scenario(context, scenario):
    context.client.close()
