from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator

from gateway_core.auth import (
    BearerCredentials,
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_core.config import settings


def _anonymous_credentials() -> BearerCredentials:
    return BearerCredentials(
        publication_url=settings.substack_base_url,
        substack_sid="",
        connect_sid="",
    )


@contextlib.asynccontextmanager
async def _public_substack_client() -> AsyncIterator[SubstackClient]:
    async with make_substack_client(_anonymous_credentials()) as sub:
        yield sub


@contextlib.asynccontextmanager
async def _public_publication_client() -> AsyncIterator[PublicationClient]:
    credentials = _anonymous_credentials()
    assert credentials.publication_url is not None
    async with make_publication_client(
        credentials, credentials.publication_url
    ) as publication:
        yield publication


@contextlib.asynccontextmanager
async def _authenticated_clients(
    token: str,
) -> AsyncIterator[tuple[PublicationClient, SubstackClient]]:
    credentials = decode_bearer_credentials(token)
    assert credentials.publication_url is not None
    async with (
        make_publication_client(
            credentials, credentials.publication_url
        ) as publication,
        make_substack_client(credentials) as substack,
    ):
        yield publication, substack
