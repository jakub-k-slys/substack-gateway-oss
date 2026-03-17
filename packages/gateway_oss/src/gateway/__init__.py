from __future__ import annotations

from typing import Any

__all__ = ["api", "mcp", "create_app"]


def __getattr__(name: str) -> Any:
    if name == "api":
        from gateway_oss.api.app import api

        return api
    if name == "mcp":
        from gateway_oss.mcp.app import mcp

        return mcp
    if name == "create_app":
        from gateway_oss.app_factory import create_app

        return create_app
    raise AttributeError(name)
