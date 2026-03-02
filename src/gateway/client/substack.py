from __future__ import annotations

from gateway.client.base import SubstackHTTPBase


class SubstackClient(SubstackHTTPBase):
    """Async Substack API client.

    Provides authenticated HTTP connectivity to Substack.  Domain logic lives
    in the service classes (``gateway.services.*``).  Use as an async context
    manager::

        async with SubstackClient(
            substack_sid=...,
            connect_sid=...,
            publication_url=...,
        ) as client:
            service = DraftsService(client)
            drafts = await service.list_drafts()
    """
