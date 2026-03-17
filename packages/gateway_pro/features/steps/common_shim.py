from __future__ import annotations

# Re-export all shared step definitions from the root features/steps/common.py
# so that pro-only feature files can use them when run as a separate suite:
#
#   uv run behave packages/gateway_pro/features/
#
# Importing the module causes behave to register all @given/@when/@then steps
# defined there into the current run's step registry.
from features.steps.common import *  # noqa: F401, F403
