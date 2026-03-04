from __future__ import annotations

import os

import httpx


def before_scenario(context, scenario):
    base_url = os.environ.get("SUBSTACK_GATEWAY_BASE_URL", "http://localhost:5001")
    context.client = httpx.Client(base_url=base_url)
    context.headers: dict[str, str] = {}
    context.response = None


def after_scenario(context, scenario):
    context.client.close()
