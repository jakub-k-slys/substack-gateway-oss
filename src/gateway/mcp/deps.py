from __future__ import annotations

import contextlib
import logging
from collections.abc import AsyncIterator

from fastmcp.dependencies import Depends
from fastmcp.server.dependencies import CurrentRequest
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


def _decode_bearer(authorization: str) -> BearerCredentials:
    """Decode a base64 Bearer token; raises ValueError if invalid."""
    raw = authorization.removeprefix("Bearer ").strip()
    return decode_bearer_credentials(raw)


async def get_credentials(request: Request = CurrentRequest()) -> BearerCredentials:
    return _decode_bearer(request.headers.get("authorization", ""))


@contextlib.asynccontextmanager
async def get_publication_client(
    credentials: BearerCredentials = Depends(get_credentials),
    request: Request = CurrentRequest(),
) -> AsyncIterator[PublicationClient]:
    publication_url = request.headers.get("x-publication-url", "")
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
