from __future__ import annotations

import contextlib
import logging
from collections.abc import AsyncIterator

from fastmcp.dependencies import Depends
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import CurrentRequest, get_access_token
from sqlalchemy import text
from starlette.requests import Request

from gateway.auth import (
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway.client.publication import PublicationClient
from gateway.client.substack import SubstackClient
from gateway.models.schemas import BearerCredentials
from gateway.services.drafts import DraftsService
from gateway.services.following import FollowingService
from gateway.services.notes import NotesService
from gateway.services.posts import PostsService
from gateway.services.profiles import ProfilesService

_log = logging.getLogger(__name__)

_HEADER_HINT = (
    "Configure your MCP client to send the following HTTP headers: "
    "'Authorization: Bearer <base64-credentials>' and "
    "'x-publication-url: <your-publication-url>'."
)


def _decode_bearer(authorization: str) -> BearerCredentials:
    """Decode a base64 Bearer token; raises ToolError if missing or invalid."""
    if not authorization:
        raise ToolError(f"Missing Authorization header. {_HEADER_HINT}")
    raw = authorization.removeprefix("Bearer ").strip()
    try:
        return decode_bearer_credentials(raw)
    except ValueError as exc:
        raise ToolError(f"Invalid Authorization header: {exc}") from exc


async def _load_user_creds(user_id: int) -> tuple[str, str] | None:
    """Return (bearer_b64, pub_url) from user_credentials, or None."""
    from gateway.oauth.db import get_engine

    async with get_engine().connect() as conn:
        row = await conn.execute(
            text("SELECT bearer, pub_url FROM user_credentials WHERE user_id = :uid"),
            {"uid": user_id},
        )
        rec = row.fetchone()
    return (rec[0], rec[1]) if rec is not None else None


async def get_credentials(request: Request = CurrentRequest()) -> BearerCredentials:
    token = get_access_token()
    if token is not None:
        user_id = (token.claims or {}).get("user_id")
        if user_id is not None:
            creds = await _load_user_creds(int(user_id))
            if creds is not None:
                bearer_b64, _pub_url = creds
                return decode_bearer_credentials(bearer_b64)
    return _decode_bearer(request.headers.get("authorization", ""))


@contextlib.asynccontextmanager
async def get_publication_client(
    credentials: BearerCredentials = Depends(get_credentials),
    request: Request = CurrentRequest(),
) -> AsyncIterator[PublicationClient]:
    token = get_access_token()
    if token is not None:
        user_id = (token.claims or {}).get("user_id")
        if user_id is not None:
            creds = await _load_user_creds(int(user_id))
            if creds is not None:
                _bearer_b64, pub_url = creds
                _log.debug("Creating PublicationClient for publication: %s", pub_url)
                async with make_publication_client(credentials, pub_url) as pub:
                    yield pub
                return
    publication_url = request.headers.get("x-publication-url", "")
    if not publication_url:
        raise ToolError(f"Missing x-publication-url header. {_HEADER_HINT}")
    _log.debug("Creating PublicationClient for publication: %s", publication_url)
    async with make_publication_client(credentials, publication_url) as pub:
        yield pub


@contextlib.asynccontextmanager
async def get_substack_client(
    credentials: BearerCredentials = Depends(get_credentials),
) -> AsyncIterator[SubstackClient]:
    _log.debug("Creating SubstackClient")
    async with make_substack_client(credentials) as sub:
        yield sub


async def get_notes_service(
    pub: PublicationClient = Depends(get_publication_client),
    sub: SubstackClient = Depends(get_substack_client),
) -> NotesService:
    return NotesService(pub, sub)


async def get_drafts_service(
    pub: PublicationClient = Depends(get_publication_client),
    sub: SubstackClient = Depends(get_substack_client),
) -> DraftsService:
    return DraftsService(pub, sub)


async def get_posts_service(
    pub: PublicationClient = Depends(get_publication_client),
    sub: SubstackClient = Depends(get_substack_client),
) -> PostsService:
    return PostsService(pub, sub)


async def get_profiles_service(
    sub: SubstackClient = Depends(get_substack_client),
) -> ProfilesService:
    return ProfilesService(sub)


async def get_following_service(
    pub: PublicationClient = Depends(get_publication_client),
    sub: SubstackClient = Depends(get_substack_client),
) -> FollowingService:
    return FollowingService(pub, sub)
