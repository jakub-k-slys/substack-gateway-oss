from __future__ import annotations

from fastmcp.dependencies import Depends
from gateway.client.publication import PublicationClient
from gateway.client.substack import SubstackClient
from gateway.mcp.deps import get_publication_client, get_substack_client

from gateway_pro.services.drafts import DraftsService


async def get_drafts_service(
    pub: PublicationClient = Depends(get_publication_client),
    sub: SubstackClient = Depends(get_substack_client),
) -> DraftsService:
    return DraftsService(pub, sub)
