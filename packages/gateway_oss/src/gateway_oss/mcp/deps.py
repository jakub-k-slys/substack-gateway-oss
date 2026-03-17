from __future__ import annotations

import contextlib
import logging
from collections.abc import AsyncIterator

from fastmcp.dependencies import Depends
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import CurrentRequest, get_access_token
from starlette.requests import Request

from gateway_oss.auth import (
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway_oss.client.publication import PublicationClient
from gateway_oss.client.substack import SubstackClient
from gateway_oss.extensions.runtime import get_runtime
from gateway_oss.models.schemas import BearerCredentials
from gateway_oss.services.following import FollowingService
from gateway_oss.services.notes import NotesService
from gateway_oss.services.posts import PostsService
from gateway_oss.services.profiles import ProfilesService

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
    provider = get_runtime().credential_provider
    if provider is None:
        return None
    return await provider.get_bearer_for_user(user_id)


async def get_credentials(request: Request = CurrentRequest()) -> BearerCredentials:
    token = get_access_token()
    if token is not None:
        user_id = (token.claims or {}).get("user_id")
        if user_id is None:
            raise ToolError(
                "OAuth token is missing the 'user_id' claim. "
                "Please re-authenticate to obtain a valid token."
            )
        creds = await _load_user_creds(int(user_id))
        if creds is None:
            raise ToolError(
                "No Substack credentials provider is configured for your account. "
                "Please configure your credentials first."
            )
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
        if user_id is None:
            raise ToolError(
                "OAuth token is missing the 'user_id' claim. "
                "Please re-authenticate to obtain a valid token."
            )
        creds = await _load_user_creds(int(user_id))
        if creds is None:
            raise ToolError(
                "No Substack credentials provider is configured for your account. "
                "Please configure your credentials first."
            )
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
