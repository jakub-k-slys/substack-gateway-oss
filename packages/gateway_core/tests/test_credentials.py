from __future__ import annotations

import pytest

from gateway_core.auth import BearerCredentials
from gateway_core.credentials import (
    MissingCredentialsError,
    get_credential_resolver,
    set_credential_resolver,
)


class _StubResolver:
    def __init__(self, credentials: BearerCredentials | None) -> None:
        self._credentials = credentials
        self.seen: list[object] = []

    async def resolve(self, access_token: object) -> BearerCredentials | None:
        self.seen.append(access_token)
        return self._credentials


@pytest.fixture(autouse=True)
def _clear_resolver():
    set_credential_resolver(None)
    yield
    set_credential_resolver(None)


def test_registry_starts_empty() -> None:
    assert get_credential_resolver() is None


def test_registry_round_trips() -> None:
    resolver = _StubResolver(None)
    set_credential_resolver(resolver)
    assert get_credential_resolver() is resolver


def test_registry_can_be_cleared() -> None:
    set_credential_resolver(_StubResolver(None))
    set_credential_resolver(None)
    assert get_credential_resolver() is None


def test_missing_credentials_error_is_actionable() -> None:
    message = str(MissingCredentialsError())
    assert "token" in message
    assert "credentials" in message.lower()


def test_missing_credentials_error_is_runtime_error() -> None:
    assert issubclass(MissingCredentialsError, RuntimeError)
