from __future__ import annotations

import importlib
import json
import pathlib
import sys

# Re-export all shared step definitions from the root features/steps/common.py
# so that pro-only feature files can use them when run as a separate suite:
#
#   uv run behave packages/gateway_pro/features/
#
# Importing the module causes behave to register all @given/@when/@then steps
# defined there into the current run's step registry.
REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from packages.gateway_oss.features.steps.common import *  # noqa: E402, F401, F403

sys.modules.setdefault(
    "common", importlib.import_module("packages.gateway_oss.features.steps.common")
)

SAMPLES_DIR = pathlib.Path(__file__).resolve().parents[2] / "samples"


def load_sample(path: str):
    return json.loads((SAMPLES_DIR / path).read_text())
