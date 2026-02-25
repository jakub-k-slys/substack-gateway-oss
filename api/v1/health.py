from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from api.deps import get_substack_client
from client.substack import SubstackClient
from models.schemas import HealthResponse, LivenessResponse

router = APIRouter(tags=["health"])


@router.get("/health/live", response_model=LivenessResponse)
async def health_live() -> LivenessResponse:
    """Public liveness probe — no auth required."""
    return LivenessResponse(status="ok")


@router.get("/health/ready", response_model=HealthResponse)
async def health_ready(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> HealthResponse:
    """Authenticated readiness probe — verifies Substack connectivity."""
    connected = await client.check_connectivity()
    return HealthResponse(connected=connected)
