from __future__ import annotations

import sys
from pathlib import Path

# Put this directory on sys.path so test modules can import the shared
# builders module (`from _dialect_helpers import ...`) as a top-level name
# under --import-mode=importlib. This directory deliberately has no
# __init__.py: with one, this conftest would register as `tests.conftest` and
# clash with gateway_stats' conftest when the full suite runs together.
sys.path.insert(0, str(Path(__file__).parent))
