from __future__ import annotations

import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from gateway.api.deps import (
    get_credentials,
    get_publication_client,
    get_substack_client,
)
from gateway.client.publication import PublicationClient
from gateway.client.substack import SubstackClient
from gateway.config import settings
from gateway.models.schemas import BearerCredentials

from gateway_pro.services.drafts import DraftsService

_log = logging.getLogger(__name__)

_INVALID_CREDENTIALS = "Invalid credentials"


def require_gateway_key(
    credentials: Annotated[BearerCredentials, Depends(get_credentials)],
) -> None:
    if credentials.gateway_key != settings.gateway_key:
        _log.warning("Rejected: invalid or missing gateway_key")
        raise HTTPException(status_code=403, detail=_INVALID_CREDENTIALS)


def get_drafts_service(
    pub: Annotated[PublicationClient, Depends(get_publication_client)],
    sub: Annotated[SubstackClient, Depends(get_substack_client)],
) -> DraftsService:
    return DraftsService(pub, sub)
