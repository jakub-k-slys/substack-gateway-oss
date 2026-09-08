from __future__ import annotations

import base64
import contextlib
from collections.abc import AsyncIterator
from urllib.parse import urlparse

from pydantic import BaseModel, ValidationError

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient


class BearerCredentials(BaseModel):
    publication_url: str | None = None
    substack_sid: str | None = None
    connect_sid: str | None = None


def validate_bearer_credentials(
    credentials: BearerCredentials, *, source: str = "Token"
) -> None:
    """Validate that credentials carry a usable publication URL and session cookies.

    Applies the same three checks regardless of where the credentials came
    from: a decoded ``token`` argument, or a value returned by an installed
    :class:`~gateway_core.credentials.CredentialResolver`. ``source`` names the
    origin in the raised message (e.g. ``"Token"`` or ``"Resolved credentials"``).

    Raises:
        ValueError: If required fields are absent or malformed.
    """
    if not credentials.publication_url:
        raise ValueError(f"{source} must contain publication_url")
    parsed = urlparse(credentials.publication_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"{source} must contain a valid HTTP or HTTPS publication_url")
    if not credentials.substack_sid or not credentials.connect_sid:
        raise ValueError(f"{source} must contain substack_sid and connect_sid")


def decode_bearer_credentials(raw: str) -> BearerCredentials:
    """Decode a base64-encoded JSON gateway token into BearerCredentials.

    Args:
        raw: Token string with any ``"Bearer "`` prefix already stripped.

    Raises:
        ValueError: If the token is not valid base64-encoded JSON credentials,
            or if required fields are absent or malformed.
    """
    try:
        decoded = base64.b64decode(raw).decode()
        credentials = BearerCredentials.model_validate_json(decoded)
    except (ValidationError, Exception) as exc:
        raise ValueError(
            "Invalid token: expected base64-encoded JSON credentials"
        ) from exc
    validate_bearer_credentials(credentials)
    return credentials


@contextlib.asynccontextmanager
async def make_publication_client(
    credentials: BearerCredentials,
    publication_url: str,
    request_id: str | None = None,
) -> AsyncIterator[PublicationClient]:
    """Yield an authenticated PublicationClient from already-decoded credentials."""
    assert credentials.substack_sid is not None
    assert credentials.connect_sid is not None
    async with PublicationClient(
        substack_sid=credentials.substack_sid,
        connect_sid=credentials.connect_sid,
        publication_url=publication_url,
        request_id=request_id,
    ) as client:
        yield client


@contextlib.asynccontextmanager
async def make_substack_client(
    credentials: BearerCredentials,
    request_id: str | None = None,
) -> AsyncIterator[SubstackClient]:
    """Yield an authenticated SubstackClient from already-decoded credentials."""
    assert credentials.substack_sid is not None
    assert credentials.connect_sid is not None
    async with SubstackClient(
        substack_sid=credentials.substack_sid,
        connect_sid=credentials.connect_sid,
        request_id=request_id,
    ) as client:
        yield client
