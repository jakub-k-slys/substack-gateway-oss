from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator

from fastmcp.server.dependencies import get_access_token

from gateway_core.auth import (
    BearerCredentials,
    decode_bearer_credentials,
    make_publication_client,
    make_substack_client,
)
from gateway_core.client.publication import PublicationClient
from gateway_core.client.substack import SubstackClient
from gateway_core.config import settings
from gateway_core.credentials import (
    MissingCredentialsError,
    get_credential_resolver,
)


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


async def resolve_credentials(token: str | None = None) -> BearerCredentials:
    """Return the caller's Substack credentials.

    An explicit ``token`` is always preferred. When it is absent, the installed
    credential resolver is asked about the authenticated caller.
    """
    if token:
        return decode_bearer_credentials(token)
    resolver = get_credential_resolver()
    if resolver is None:
        raise MissingCredentialsError()
    credentials = await resolver.resolve(get_access_token())
    if credentials is None:
        raise MissingCredentialsError()
    return credentials


@contextlib.asynccontextmanager
async def clients_from(
    credentials: BearerCredentials,
) -> AsyncIterator[tuple[PublicationClient, SubstackClient]]:
    """Yield clients built from credentials that are already resolved."""
    assert credentials.publication_url is not None
    async with (
        make_publication_client(
            credentials, credentials.publication_url
        ) as publication,
        make_substack_client(credentials) as substack,
    ):
        yield publication, substack


@contextlib.asynccontextmanager
async def _authenticated_clients(
    token: str | None = None,
) -> AsyncIterator[tuple[PublicationClient, SubstackClient]]:
    credentials = await resolve_credentials(token)
    async with clients_from(credentials) as clients:
        yield clients
