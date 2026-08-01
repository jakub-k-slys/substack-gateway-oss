from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request

from gateway_core.auth import (
    BearerCredentials,
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient

_log = logging.getLogger(__name__)


_INVALID_CREDENTIALS = "Invalid credentials"


def _decode_gateway_token(token: str) -> BearerCredentials:
    """Decode a base64 gateway token and return parsed credentials."""
    raw = token.strip()
    if not raw:
        _log.warning("Rejected: empty x-gateway-token header")
        raise HTTPException(status_code=401, detail=_INVALID_CREDENTIALS)
    try:
        return decode_bearer_credentials(raw)
    except ValueError:
        _log.warning("Rejected: x-gateway-token is not valid base64-encoded JSON")
        raise HTTPException(status_code=401, detail=_INVALID_CREDENTIALS)


def get_credentials(
    x_gateway_token: Annotated[str, Header(alias="x-gateway-token")],
) -> BearerCredentials:
    return _decode_gateway_token(x_gateway_token)


async def get_publication_client(
    request: Request,
    credentials: Annotated[BearerCredentials, Depends(get_credentials)],
) -> AsyncGenerator[PublicationClient, None]:
    assert credentials.publication_url is not None
    request_id: str | None = getattr(request.state, "request_id", None)
    _log.debug(
        "Creating PublicationClient for publication: %s", credentials.publication_url
    )
    async with make_publication_client(
        credentials, credentials.publication_url, request_id
    ) as client:
        yield client


async def get_substack_client(
    request: Request,
    credentials: Annotated[BearerCredentials, Depends(get_credentials)],
) -> AsyncGenerator[SubstackClient, None]:
    request_id: str | None = getattr(request.state, "request_id", None)
    _log.debug("Creating SubstackClient")
    async with make_substack_client(credentials, request_id) as client:
        yield client
