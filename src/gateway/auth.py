from __future__ import annotations

import base64
import contextlib
from collections.abc import AsyncGenerator

from pydantic import ValidationError

from gateway.client.substack import SubstackClient
from gateway.models.schemas import BearerCredentials


def decode_bearer_credentials(raw: str) -> BearerCredentials:
    """Decode a base64-encoded JSON Bearer token into BearerCredentials.

    Args:
        raw: Token string with any ``"Bearer "`` prefix already stripped.

    Raises:
        ValueError: If the token is not valid base64-encoded JSON credentials,
            or if ``substack_sid`` / ``connect_sid`` are absent.
    """
    try:
        decoded = base64.b64decode(raw).decode()
        credentials = BearerCredentials.model_validate_json(decoded)
    except (ValidationError, Exception) as exc:
        raise ValueError(
            "Invalid token: expected base64-encoded JSON credentials"
        ) from exc
    if not credentials.substack_sid or not credentials.connect_sid:
        raise ValueError("Token must contain substack_sid and connect_sid")
    return credentials


@contextlib.asynccontextmanager
async def make_substack_client(
    credentials: BearerCredentials,
    publication_url: str,
    request_id: str | None = None,
) -> AsyncGenerator[SubstackClient, None]:
    """Yield an authenticated SubstackClient from already-decoded credentials.

    Both the REST API (``api/deps.py``) and the MCP server (``mcp/app.py``)
    use this as the single place that maps ``BearerCredentials`` + a
    publication URL into a live ``SubstackClient``.
    """
    assert (
        credentials.substack_sid is not None
    )  # guaranteed by decode_bearer_credentials
    assert (
        credentials.connect_sid is not None
    )  # guaranteed by decode_bearer_credentials
    async with SubstackClient(
        substack_sid=credentials.substack_sid,
        connect_sid=credentials.connect_sid,
        publication_url=publication_url,
        request_id=request_id,
    ) as client:
        yield client
