from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from gateway_mcp_common.clients import (
    _anonymous_credentials,  # noqa: F401
    _authenticated_clients,  # noqa: F401
)
from gateway_oss.extensions.runtime import get_runtime

runtime = get_runtime()

_mcp = FastMCP("substack-gateway", auth=runtime.mcp_auth_provider)


def register_authenticated_tools(mcp: FastMCP) -> None:
    """Backward-compatibility no-op.

    The authenticated OSS tools are now registered via the capability
    registry (entry-point group ``substack_gateway.capabilities``). This
    function is retained because a downstream extension imports and calls it;
    it must NOT register anything, or those tools would be double-registered
    (FastMCP raises on duplicate tool names).
    """


_mcp_app: Any = None


def _build_mcp_app() -> Any:
    from gateway_oss.registry import load_mcp_capabilities

    for cap in load_mcp_capabilities():
        cap.register(_mcp)
    for extension in runtime.extensions:
        extension.register_mcp(_mcp, runtime.context)
    return _mcp.http_app(transport="streamable-http", path="/", stateless_http=True)


def __getattr__(name: str) -> Any:
    # Build the MCP ASGI app lazily: extension registration must not run at
    # import time. An extension's register_mcp imports gateway_pro.mcp.app,
    # which imports this module back — doing that during import would re-enter
    # a partially-initialised module and raise a circular ImportError.
    if name == "mcp":
        global _mcp_app
        if _mcp_app is None:
            _mcp_app = _build_mcp_app()
        return _mcp_app
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
