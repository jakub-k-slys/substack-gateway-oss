from __future__ import annotations

from typing import Any

from gateway_core.versioning import get_application_version, get_package_version

__version__ = get_package_version("gateway_oss")
__app_version__ = get_application_version(fallback=__version__)

__all__ = ["api", "mcp", "create_app", "__version__", "__app_version__"]


def __getattr__(name: str) -> Any:
    if name == "api":
        from substack_gateway.api_app import api

        return api
    if name == "mcp":
        from substack_gateway.mcp_app import mcp

        return mcp
    if name == "create_app":
        from substack_gateway.app_factory import create_app

        return create_app
    raise AttributeError(name)
