from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Header, HTTPException

from client.substack import SubstackClient

_log = logging.getLogger(__name__)


async def get_substack_client(
    authorization: Annotated[str, Header()],
    x_publication_url: Annotated[str, Header()],
) -> AsyncGenerator[SubstackClient, None]:
    if not authorization.startswith("Bearer "):
        _log.warning(
            "Rejected: malformed Authorization header (missing 'Bearer ' prefix)"
        )
        raise HTTPException(
            status_code=401,
            detail="Authorization header must be 'Bearer <substack-session-token>'",
        )
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        _log.warning("Rejected: empty Bearer token in Authorization header")
        raise HTTPException(
            status_code=401,
            detail="Bearer token must not be empty",
        )
    if not x_publication_url.startswith(("http://", "https://")):
        _log.warning("Rejected: invalid x-publication-url %r", x_publication_url)
        raise HTTPException(
            status_code=400,
            detail="x-publication-url must be a valid HTTP or HTTPS URL",
        )
    _log.debug("Creating SubstackClient for publication: %s", x_publication_url)
    async with SubstackClient(token=token, publication_url=x_publication_url) as client:
        yield client
