from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_posts.service import (
    PostReactionsService,
    PostRestacksService,
    PostsService,
)
from gateway_rest_common.deps import get_publication_client, get_substack_client


def get_posts_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> PostsService:
    return PostsService(pub, sub)


def get_post_reactions_service(
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> PostReactionsService:
    return PostReactionsService(sub)


def get_post_restacks_service(
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> PostRestacksService:
    return PostRestacksService(sub)
