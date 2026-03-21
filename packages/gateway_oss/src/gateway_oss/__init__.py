from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from typing import Any

try:
    __version__ = version("gateway_oss")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["api", "mcp", "create_app", "__version__"]


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
