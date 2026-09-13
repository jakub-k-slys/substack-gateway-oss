from __future__ import annotations

import tomllib
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_BANNED = ("aiocache", "redis")


def _oss_pyprojects() -> list[Path]:
    found = [_ROOT / "pyproject.toml"]
    for path in sorted((_ROOT / "packages").glob("*/pyproject.toml")):
        if "gateway_pro" in path.parts:
            continue  # not part of this repository
        found.append(path)
    return found


def test_no_oss_package_declares_a_caching_dependency() -> None:
    offenders: list[str] = []
    for path in _oss_pyprojects():
        data = tomllib.loads(path.read_text())
        deps = data.get("project", {}).get("dependencies", [])
        for dep in deps:
            if any(dep.startswith(banned) for banned in _BANNED):
                offenders.append(f"{path.relative_to(_ROOT)}: {dep}")
    assert offenders == [], (
        "caching is an extension concern; these declarations bring it back: "
        + ", ".join(offenders)
    )


def test_no_oss_source_file_imports_a_caching_library() -> None:
    offenders: list[str] = []
    roots = [_ROOT / "src"] + [
        p for p in (_ROOT / "packages").glob("*/src") if "gateway_pro" not in p.parts
    ]
    for root in roots:
        for path in root.rglob("*.py"):
            text = path.read_text()
            for banned in _BANNED:
                if f"import {banned}" in text or f"from {banned}" in text:
                    offenders.append(f"{path.relative_to(_ROOT)}: {banned}")
    assert offenders == [], "caching library imported in OSS: " + ", ".join(offenders)
