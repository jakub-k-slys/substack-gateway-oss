from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_substack_client
from client.exceptions import SubstackAPIError, SubstackAuthError
from client.substack import SubstackClient
from models.schemas import ProfileResponse

router = APIRouter()


@router.get("/me", response_model=ProfileResponse)
async def get_me(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> ProfileResponse:
    try:
        raw = await client.get_own_profile()
    except SubstackAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SubstackAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return ProfileResponse.from_raw(raw)
