from __future__ import annotations

# Re-export the OSS MCP step definitions (Given and Then steps) so they are
# available in the pro feature suite when run as a separate behave invocation:
#
#   uv run behave packages/gateway_pro/features/
#
from features.steps.mcp_tools import *  # noqa: F401, F403
