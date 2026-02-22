from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Header, HTTPException

from client.substack import SubstackClient


async def get_substack_client(
    authorization: Annotated[str, Header()],
    x_publication_url: Annotated[str, Header()],
) -> AsyncGenerator[SubstackClient, None]:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization header must be 'Bearer <substack-session-token>'",
        )
    token = authorization.removeprefix("Bearer ")
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Bearer token must not be empty",
        )
    if not x_publication_url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=400,
            detail="x-publication-url must be a valid HTTP or HTTPS URL",
        )
    async with SubstackClient(token=token, publication_url=x_publication_url) as client:
        yield client
