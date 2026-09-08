from __future__ import annotations

import base64
import json

import pytest

from gateway_core.auth import BearerCredentials
from gateway_core.credentials import MissingCredentialsError, set_credential_resolver
from gateway_mcp_common.clients import resolve_credentials

_EXPLICIT = BearerCredentials(
    publication_url="https://explicit.substack.com",
    substack_sid="explicit-sid",
    connect_sid="explicit-connect",
)
_RESOLVED = BearerCredentials(
    publication_url="https://resolved.substack.com",
    substack_sid="resolved-sid",
    connect_sid="resolved-connect",
)


def _encode(credentials: BearerCredentials) -> str:
    return base64.b64encode(json.dumps(credentials.model_dump()).encode()).decode()


class _StubResolver:
    def __init__(self, credentials: BearerCredentials | None) -> None:
        self._credentials = credentials
        self.calls = 0

    async def resolve(self, access_token: object) -> BearerCredentials | None:
        self.calls += 1
        return self._credentials


@pytest.fixture(autouse=True)
def _clear_resolver():
    set_credential_resolver(None)
    yield
    set_credential_resolver(None)


@pytest.mark.anyio
async def test_explicit_token_is_decoded() -> None:
    result = await resolve_credentials(_encode(_EXPLICIT))
    assert result.publication_url == "https://explicit.substack.com"
    assert result.substack_sid == "explicit-sid"


@pytest.mark.anyio
async def test_explicit_token_wins_over_resolver() -> None:
    resolver = _StubResolver(_RESOLVED)
    set_credential_resolver(resolver)
    result = await resolve_credentials(_encode(_EXPLICIT))
    assert result.publication_url == "https://explicit.substack.com"
    assert resolver.calls == 0


@pytest.mark.anyio
async def test_resolver_used_when_token_omitted() -> None:
    resolver = _StubResolver(_RESOLVED)
    set_credential_resolver(resolver)
    result = await resolve_credentials()
    assert result.publication_url == "https://resolved.substack.com"
    assert resolver.calls == 1


@pytest.mark.anyio
async def test_no_resolver_raises() -> None:
    with pytest.raises(MissingCredentialsError):
        await resolve_credentials()


@pytest.mark.anyio
async def test_resolver_returning_none_raises() -> None:
    set_credential_resolver(_StubResolver(None))
    with pytest.raises(MissingCredentialsError):
        await resolve_credentials()


@pytest.mark.anyio
async def test_empty_token_string_is_treated_as_omitted() -> None:
    resolver = _StubResolver(_RESOLVED)
    set_credential_resolver(resolver)
    result = await resolve_credentials("")
    assert result.publication_url == "https://resolved.substack.com"
    assert resolver.calls == 1
