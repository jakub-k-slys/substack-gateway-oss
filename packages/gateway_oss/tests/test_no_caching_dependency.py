from __future__ import annotations

import tomllib
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_THIS_FILE = Path(__file__).resolve()
_BANNED = ("aiocache", "redis")

# Directories that never carry OSS-relevant Python or manifests: VCS/tooling
# caches, build artifacts, and virtualenvs.
_SKIP_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "dist",
    "build",
    "__pycache__",
    ".ruff_cache",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
}


def _is_pro_or_skipped(path: Path) -> bool:
    if "gateway_pro" in path.parts:
        return True  # not part of this repository
    return any(part in _SKIP_DIR_NAMES for part in path.parts)


def _oss_pyprojects() -> list[Path]:
    found = [_ROOT / "pyproject.toml"]
    for path in sorted((_ROOT / "packages").glob("*/pyproject.toml")):
        if _is_pro_or_skipped(path):
            continue
        found.append(path)
    return found


def _dependency_strings(data: dict) -> list[str]:
    """Every dependency specifier declared in any table of a pyproject."""
    deps: list[str] = []

    project = data.get("project", {})
    deps.extend(project.get("dependencies", []))
    for extra_deps in project.get("optional-dependencies", {}).values():
        deps.extend(extra_deps)

    for group_entries in data.get("dependency-groups", {}).values():
        for entry in group_entries:
            # Entries are either plain requirement strings or
            # {"include-group": "<other-group>"} references (PEP 735).
            if isinstance(entry, str):
                deps.append(entry)

    return deps


def test_no_oss_package_declares_a_caching_dependency() -> None:
    offenders: list[str] = []
    for path in _oss_pyprojects():
        data = tomllib.loads(path.read_text())
        for dep in _dependency_strings(data):
            if any(dep.startswith(banned) for banned in _BANNED):
                offenders.append(f"{path.relative_to(_ROOT)}: {dep}")
    assert offenders == [], (
        "caching is an extension concern; these declarations bring it back: "
        + ", ".join(offenders)
    )


def test_no_oss_source_file_imports_a_caching_library() -> None:
    offenders: list[str] = []
    for path in _ROOT.rglob("*.py"):
        if _is_pro_or_skipped(path):
            continue
        if path.resolve() == _THIS_FILE:
            continue  # this file legitimately mentions the banned names
        text = path.read_text()
        for banned in _BANNED:
            if f"import {banned}" in text or f"from {banned}" in text:
                offenders.append(f"{path.relative_to(_ROOT)}: {banned}")
    assert offenders == [], "caching library imported in OSS: " + ", ".join(offenders)
