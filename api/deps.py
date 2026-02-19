from __future__ import annotations

from typing import Annotated

from fastapi import Header, HTTPException

from client.substack import SubstackClient


async def get_substack_client(
    authorization: Annotated[str, Header()],
    x_publication_url: Annotated[str, Header()],
) -> SubstackClient:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization header must be 'Bearer <substack-session-token>'",
        )
    token = authorization.removeprefix("Bearer ")
    return SubstackClient(token=token, publication_url=x_publication_url)
