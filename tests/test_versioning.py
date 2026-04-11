from __future__ import annotations

from pathlib import Path

from gateway_oss.versioning import (
    _find_project_pyproject,
    _read_project_version,
    get_application_version,
)


def test_read_project_version_returns_substack_gateway_version(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """
[project]
name = "substack-gateway"
version = "0.11.0"
""".strip()
    )

    assert _read_project_version(pyproject, project_name="substack-gateway") == "0.11.0"


def test_find_project_pyproject_matches_requested_project_name(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    nested = repo_root / "packages" / "gateway_oss" / "src" / "gateway_oss"
    nested.mkdir(parents=True)
    package_pyproject = repo_root / "packages" / "gateway_oss" / "pyproject.toml"
    package_pyproject.parent.mkdir(parents=True, exist_ok=True)
    package_pyproject.write_text(
        """
[project]
name = "gateway_oss"
version = "0.5.0"
""".strip()
    )
    pyproject = repo_root / "pyproject.toml"
    pyproject.write_text(
        """
[project]
name = "substack-gateway"
version = "0.11.0"
""".strip()
    )

    init_file = nested / "__init__.py"
    init_file.write_text("")

    assert (
        _find_project_pyproject(init_file, project_name="substack-gateway") == pyproject
    )


def test_get_application_version_prefers_env_override(monkeypatch) -> None:
    monkeypatch.setenv("SUBSTACK_GATEWAY_VERSION", "0.12.0")

    assert get_application_version(fallback="0.5.0") == "0.12.0"
