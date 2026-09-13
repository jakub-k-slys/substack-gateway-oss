from __future__ import annotations

import ast
import pathlib

import pytest

from gateway_core.config import Settings


def test_admin_token_has_no_default() -> None:
    assert Settings().admin_token is None


def test_admin_token_reads_its_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUBSTACK_GATEWAY_ADMIN_TOKEN", "s3cret")
    assert Settings().admin_token == "s3cret"


def test_no_setting_ships_a_built_in_secret() -> None:
    """A default on a credential setting is a published credential.

    This guards the whole Settings class rather than one field: any future
    setting whose name marks it as a secret must be introduced without a
    literal default, or it ends up readable by everyone who can read this
    repository.
    """
    import gateway_core.config as module

    source = pathlib.Path(module.__file__).read_text()
    tree = ast.parse(source)
    cls = next(
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.ClassDef) and n.name == "Settings"
    )

    offenders = [
        node.target.id
        for node in cls.body
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and any(
            mark in node.target.id
            for mark in ("token", "secret", "password", "key", "credential")
        )
        and isinstance(node.value, ast.Constant)
        and node.value.value is not None
    ]
    assert offenders == [], (
        "these credential settings carry a built-in default, which publishes "
        "them to every reader of this repository: " + ", ".join(offenders)
    )
