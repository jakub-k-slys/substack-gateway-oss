from __future__ import annotations

import re
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

_PROJECT_NAME_RE = re.compile(r'^name\s*=\s*"(?P<name>[^"]+)"\s*$')
_PROJECT_VERSION_RE = re.compile(r'^version\s*=\s*"(?P<version>[^"]+)"\s*$')


def get_package_version(package_name: str, *, fallback: str = "0.0.0") -> str:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return fallback


def get_application_version(*, fallback: str) -> str:
    try:
        return version("substack-gateway")
    except PackageNotFoundError:
        pyproject = _find_project_pyproject(
            Path(__file__).resolve(),
            project_name="substack-gateway",
        )
        if pyproject is None:
            return fallback
        resolved = _read_project_version(pyproject, project_name="substack-gateway")
        return resolved or fallback


def _find_project_pyproject(start: Path, *, project_name: str) -> Path | None:
    for parent in start.parents:
        candidate = parent / "pyproject.toml"
        if candidate.is_file() and _read_project_name(candidate) == project_name:
            return candidate
    return None


def _read_project_name(pyproject: Path) -> str | None:
    project_section = False

    for raw_line in pyproject.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("["):
            project_section = line == "[project]"
            continue
        if not project_section:
            continue

        name_match = _PROJECT_NAME_RE.match(line)
        if name_match is not None:
            return name_match.group("name")

    return None


def _read_project_version(pyproject: Path, *, project_name: str) -> str | None:
    project_section = False
    matched_name = False

    for raw_line in pyproject.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("["):
            project_section = line == "[project]"
            if not project_section:
                matched_name = False
            continue
        if not project_section:
            continue

        if not matched_name:
            name_match = _PROJECT_NAME_RE.match(line)
            if name_match is not None:
                matched_name = name_match.group("name") == project_name
            continue

        version_match = _PROJECT_VERSION_RE.match(line)
        if version_match is not None:
            return version_match.group("version")

    return None
