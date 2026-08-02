from __future__ import annotations

from fastmcp import FastMCP

from gateway_mcp_common.clients import (
    _anonymous_credentials,  # noqa: F401
    _authenticated_clients,  # noqa: F401
)

__all__ = [
    "_anonymous_credentials",
    "_authenticated_clients",
    "register_authenticated_tools",
]


def register_authenticated_tools(mcp: FastMCP) -> None:
    """Backward-compatibility no-op.

    The authenticated OSS tools are now registered via the capability
    registry (entry-point group ``substack_gateway.capabilities``). This
    function is retained because a downstream extension imports and calls it;
    it must NOT register anything, or those tools would be double-registered
    (FastMCP raises on duplicate tool names).
    """
