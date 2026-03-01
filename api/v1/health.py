from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from api.deps import get_credentials, get_substack_client
from client.substack import SubstackClient
from models.schemas import (
    BearerCredentials,
    HealthResponse,
    LivenessResponse,
    TokensInfo,
)

router = APIRouter(tags=["health"])


@router.get("/health/live", response_model=LivenessResponse)
async def health_live() -> LivenessResponse:
    """Public liveness probe — no auth required."""
    return LivenessResponse(status="ok")


@router.get(
    "/health/ready", response_model=HealthResponse, response_model_exclude_none=True
)
async def health_ready(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
    credentials: Annotated[BearerCredentials, Depends(get_credentials)],
    show: bool = False,
) -> HealthResponse:
    """Authenticated readiness probe — verifies Substack connectivity."""
    connected = await client.check_connectivity()
    return HealthResponse(
        connected=connected,
        tokens=TokensInfo(
            substack_sid=credentials.substack_sid,
            connect_sid=credentials.connect_sid,
            gateway_key=credentials.gateway_key,
        )
        if show
        else None,
    )
