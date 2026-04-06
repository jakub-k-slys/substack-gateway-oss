from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from gateway_oss.api.deps import get_publication_client, get_substack_client
from gateway_oss.client.publication import PublicationClient
from gateway_oss.client.substack import SubstackClient
from gateway_oss.services.following import FollowingService

from gateway_pro.services.drafts import DraftsService
from gateway_pro.services.following_feed import FollowingFeedService
from gateway_pro.services.note_reactions import NoteReactionsService
from gateway_pro.services.post_reactions import PostReactionsService
from gateway_pro.services.post_restacks import PostRestacksService
from gateway_pro.services.profile_feed import ProfileFeedService


def get_drafts_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> DraftsService:
    return DraftsService(pub, sub)


def get_note_reactions_service(
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> NoteReactionsService:
    return NoteReactionsService(sub)


def get_post_reactions_service(
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> PostReactionsService:
    return PostReactionsService(sub)


def get_post_restacks_service(
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> PostRestacksService:
    return PostRestacksService(sub)


def get_profile_feed_service(
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> ProfileFeedService:
    return ProfileFeedService(sub)


def get_following_feed_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> FollowingFeedService:
    return FollowingFeedService(
        FollowingService(pub, sub),
        ProfileFeedService(sub),
    )
