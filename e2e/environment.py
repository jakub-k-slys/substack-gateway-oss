from __future__ import annotations

import os

import httpx


def before_scenario(context, scenario):
    base_url = os.environ.get("SUBSTACK_GATEWAY_BASE_URL") or "http://localhost:5001"
    timeout_sec = float(os.environ.get("SUBSTACK_GATEWAY_E2E_TIMEOUT_SEC", "120"))
    context.client = httpx.Client(
        base_url=base_url,
        timeout=httpx.Timeout(timeout_sec),
    )
    context.headers: dict[str, str] = {}
    context.response = None


def after_scenario(context, scenario):
    context.client.close()
