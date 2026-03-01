from __future__ import annotations

import base64
import logging
from collections.abc import AsyncGenerator
from typing import Annotated
from urllib.parse import urlparse

from fastapi import Depends, Header, HTTPException, Request
from pydantic import ValidationError

from client.substack import SubstackClient
from models.schemas import BearerCredentials

_log = logging.getLogger(__name__)


def _decode_bearer(authorization: str) -> BearerCredentials:
    """Decode a base64 Bearer token and return parsed credentials."""
    if not authorization.startswith("Bearer "):
        _log.warning(
            "Rejected: malformed Authorization header (missing 'Bearer ' prefix)"
        )
        raise HTTPException(
            status_code=401,
            detail="Authorization header must be 'Bearer <base64-encoded-credentials>'",
        )
    raw = authorization.removeprefix("Bearer ").strip()
    if not raw:
        _log.warning("Rejected: empty Bearer token in Authorization header")
        raise HTTPException(
            status_code=401,
            detail="Bearer token must not be empty",
        )
    try:
        decoded = base64.b64decode(raw).decode()
        credentials = BearerCredentials.model_validate_json(decoded)
    except (ValidationError, Exception):
        _log.warning("Rejected: Bearer token is not valid base64-encoded JSON")
        raise HTTPException(
            status_code=401,
            detail="Bearer token must be a base64-encoded JSON credentials object",
        )
    if not credentials.substack_sid or not credentials.connect_sid:
        _log.warning("Rejected: credentials missing substack_sid or connect_sid")
        raise HTTPException(
            status_code=401,
            detail="Credentials must include 'substack_sid' and 'connect_sid'",
        )
    return credentials


def get_credentials(
    authorization: Annotated[str, Header()],
) -> BearerCredentials:
    return _decode_bearer(authorization)


async def get_substack_client(
    request: Request,
    credentials: Annotated[BearerCredentials, Depends(get_credentials)],
    x_publication_url: Annotated[str, Header()],
) -> AsyncGenerator[SubstackClient, None]:
    assert credentials.substack_sid is not None  # guaranteed by get_credentials
    assert credentials.connect_sid is not None  # guaranteed by get_credentials
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
    async with SubstackClient(
        substack_sid=credentials.substack_sid,
        connect_sid=credentials.connect_sid,
        publication_url=x_publication_url,
        request_id=request_id,
    ) as client:
        yield client
