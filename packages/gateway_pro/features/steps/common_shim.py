from __future__ import annotations

import json
import pathlib

# Re-export all shared step definitions from the root features/steps/common.py
# so that pro-only feature files can use them when run as a separate suite:
#
#   uv run behave packages/gateway_pro/features/
#
# Importing the module causes behave to register all @given/@when/@then steps
# defined there into the current run's step registry.
from packages.gateway_oss.features.steps.common import *  # noqa: F401, F403

SAMPLES_DIR = pathlib.Path(__file__).resolve().parents[2] / "samples"


def load_sample(path: str):
    return json.loads((SAMPLES_DIR / path).read_text())
