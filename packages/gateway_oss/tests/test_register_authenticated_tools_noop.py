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


def test_register_authenticated_tools_noop_on_populated_registry_app() -> None:
    """Building the real MCP app populates it with the registry tools; then
    the extension-style call to register_authenticated_tools must not raise
    a duplicate-tool error."""
    mcp_app._build_mcp_app()
    mcp_app.register_authenticated_tools(mcp_app._mcp)  # must not raise
