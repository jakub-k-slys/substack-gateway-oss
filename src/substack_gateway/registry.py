from __future__ import annotations

import importlib.metadata

from gateway_core.capabilities import McpCapability, RestCapability

CAPABILITY_GROUP = "substack_gateway.capabilities"


def _load_all() -> list[object]:
    caps: list[object] = []
    for ep in importlib.metadata.entry_points(group=CAPABILITY_GROUP):
        factory = ep.load()
        caps.append(factory())
    return caps


def load_rest_capabilities() -> list[RestCapability]:
    return [c for c in _load_all() if isinstance(c, RestCapability)]


def load_mcp_capabilities() -> list[McpCapability]:
    return [c for c in _load_all() if isinstance(c, McpCapability)]
