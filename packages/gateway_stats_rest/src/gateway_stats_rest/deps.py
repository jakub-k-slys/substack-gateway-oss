from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from gateway_core.auth import BearerCredentials
from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_rest_common.deps import (
    get_credentials,
    get_publication_client,
    get_substack_client,
)
from gateway_stats.cache import create_stats_cache
from gateway_stats.post_stats import PostStatsService
from gateway_stats.service import StatsService


def get_stats_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
    credentials: Annotated[BearerCredentials, Depends(get_credentials)],
) -> StatsService:
    assert credentials.publication_url is not None
    return StatsService(pub, sub, create_stats_cache(), credentials.publication_url)


def get_post_stats_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
    credentials: Annotated[BearerCredentials, Depends(get_credentials)],
) -> PostStatsService:
    assert credentials.publication_url is not None
    return PostStatsService(pub, sub, create_stats_cache(), credentials.publication_url)
