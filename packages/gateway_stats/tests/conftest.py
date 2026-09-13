from __future__ import annotations

import sys
from pathlib import Path

# Every package's test directory is named "tests" with its own __init__.py,
# so relative imports like `from ._fakes import ...` resolve against whichever
# "tests" package Python's import system registered first when the full suite
# runs together (--import-mode=importlib has no per-package namespacing here).
# Put this directory on sys.path directly so test modules can import the local
# fixtures module unambiguously as a top-level name.
sys.path.insert(0, str(Path(__file__).parent))
