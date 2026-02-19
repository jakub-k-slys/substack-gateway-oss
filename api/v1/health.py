from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from api.deps import get_substack_client
from client.substack import SubstackClient
from models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> HealthResponse:
    connected = await client.check_connectivity()
    return HealthResponse(connected=connected)
