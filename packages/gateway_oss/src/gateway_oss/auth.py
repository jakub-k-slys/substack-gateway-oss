from __future__ import annotations

import base64
import contextlib
from collections.abc import AsyncIterator
from urllib.parse import urlparse

from pydantic import ValidationError

from gateway_oss.client.publication import PublicationClient
from gateway_oss.client.substack import SubstackClient
from gateway_oss.models.schemas import BearerCredentials


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
    if not credentials.publication_url:
        raise ValueError("Token must contain publication_url")
    parsed = urlparse(credentials.publication_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Token must contain a valid HTTP or HTTPS publication_url")
    if not credentials.substack_sid or not credentials.connect_sid:
        raise ValueError("Token must contain substack_sid and connect_sid")
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
