from __future__ import annotations

# Delegate to the root environment so both OSS and pro feature suites share
# identical setup/teardown logic.  Run from the project root:
#
#   uv run behave packages/gateway_pro/features/
#
from packages.gateway_oss.features.environment import after_scenario, before_scenario

__all__ = ["before_scenario", "after_scenario"]
