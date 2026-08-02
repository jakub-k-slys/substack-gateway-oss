from __future__ import annotations

from substack_gateway import mcp_app


def test_register_authenticated_tools_noop_on_populated_registry_app() -> None:
    """Building the real MCP app populates it with the registry tools; then the
    extension-style backward-compat call must not raise a duplicate-tool error."""
    from gateway_oss.mcp.app import register_authenticated_tools

    mcp_app._build_mcp_app()
    register_authenticated_tools(mcp_app._mcp)  # must not raise
