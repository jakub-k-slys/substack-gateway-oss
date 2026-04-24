from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request

from gateway_oss.auth import (
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway_oss.client.publication import PublicationClient
from gateway_oss.client.substack import SubstackClient
from gateway_oss.models.schemas import BearerCredentials
from gateway_oss.services.following import FollowingService
from gateway_oss.services.notes import NotesService
from gateway_oss.services.posts import PostsService
from gateway_oss.services.profiles import ProfilesService

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


def get_notes_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> NotesService:
    return NotesService(pub, sub)


def get_posts_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> PostsService:
    return PostsService(pub, sub)


def get_profiles_service(
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> ProfilesService:
    return ProfilesService(sub)


def get_following_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> FollowingService:
    return FollowingService(pub, sub)
