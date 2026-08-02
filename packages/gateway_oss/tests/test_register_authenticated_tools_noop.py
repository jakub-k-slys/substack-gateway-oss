from __future__ import annotations

from fastmcp import FastMCP

from gateway_oss.mcp import app as mcp_app


def test_register_authenticated_tools_registers_nothing() -> None:
    """It must be a no-op: a downstream extension calls it, and the tools
    are now registered via the capability registry, so registering here
    would double-register (FastMCP raises on duplicate tool names)."""
    server = FastMCP("test")
    mcp_app.register_authenticated_tools(server)
    # calling it again must also not raise (idempotent no-op)
    mcp_app.register_authenticated_tools(server)
