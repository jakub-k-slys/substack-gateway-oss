from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from gateway_oss.client.publication import PublicationClient
from gateway_oss.client.substack import SubstackClient
from gateway_oss.services.following import FollowingService
from gateway_oss.services.notes import NotesService
from gateway_oss.services.posts import PostsService
from gateway_oss.services.profiles import ProfilesService
from gateway_rest_common.deps import (  # noqa: F401
    _decode_gateway_token,
    get_credentials,
    get_publication_client,
    get_substack_client,
)


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
