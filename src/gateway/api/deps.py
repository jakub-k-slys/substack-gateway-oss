from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from typing import Annotated
from urllib.parse import urlparse

from fastapi import Depends, Header, HTTPException, Request

from gateway.auth import decode_bearer_credentials, make_substack_client
from gateway.client.substack import SubstackClient
from gateway.config import settings
from gateway.models.schemas import BearerCredentials

_log = logging.getLogger(__name__)


_INVALID_CREDENTIALS = "Invalid credentials"


def _decode_bearer(authorization: str) -> BearerCredentials:
    """Decode a base64 Bearer token and return parsed credentials."""
    if not authorization.startswith("Bearer "):
        _log.warning(
            "Rejected: malformed Authorization header (missing 'Bearer ' prefix)"
        )
        raise HTTPException(status_code=401, detail=_INVALID_CREDENTIALS)
    raw = authorization.removeprefix("Bearer ").strip()
    if not raw:
        _log.warning("Rejected: empty Bearer token in Authorization header")
        raise HTTPException(status_code=401, detail=_INVALID_CREDENTIALS)
    try:
        return decode_bearer_credentials(raw)
    except ValueError:
        _log.warning("Rejected: Bearer token is not valid base64-encoded JSON")
        raise HTTPException(status_code=401, detail=_INVALID_CREDENTIALS)


def get_credentials(
    authorization: Annotated[str, Header()],
) -> BearerCredentials:
    return _decode_bearer(authorization)


def require_gateway_key(
    credentials: Annotated[BearerCredentials, Depends(get_credentials)],
) -> None:
    if credentials.gateway_key != settings.gateway_key:
        _log.warning("Rejected: invalid or missing gateway_key")
        raise HTTPException(status_code=403, detail=_INVALID_CREDENTIALS)


async def get_substack_client(
    request: Request,
    credentials: Annotated[BearerCredentials, Depends(get_credentials)],
    x_publication_url: Annotated[str, Header()],
) -> AsyncGenerator[SubstackClient, None]:
    _parsed = urlparse(x_publication_url)
    if _parsed.scheme not in ("http", "https") or not _parsed.netloc:
        _log.warning("Rejected: invalid x-publication-url %r", x_publication_url)
        raise HTTPException(
            status_code=400,
            detail="x-publication-url must be a valid HTTP or HTTPS URL",
        )
    request_id: str | None = getattr(request.state, "request_id", None)
    _log.debug("gateway_key=%r", credentials.gateway_key)
    _log.debug("Creating SubstackClient for publication: %s", x_publication_url)
    async with make_substack_client(
        credentials, x_publication_url, request_id
    ) as client:
        yield client
