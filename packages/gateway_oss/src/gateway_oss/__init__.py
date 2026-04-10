from __future__ import annotations

from typing import Any

from gateway_oss.versioning import get_application_version, get_package_version

__version__ = get_package_version("gateway_oss")
__app_version__ = get_application_version(fallback=__version__)

__all__ = ["api", "mcp", "create_app", "__version__", "__app_version__"]


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
