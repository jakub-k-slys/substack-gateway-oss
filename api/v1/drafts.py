from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from api.deps import get_substack_client, require_gateway_key
from client.substack import SubstackClient
from models.schemas import CreateDraftRequest, CreateDraftResponse

router = APIRouter(tags=["drafts"])


@router.post(
    "/drafts",
    response_model=CreateDraftResponse,
    status_code=201,
    dependencies=[Depends(require_gateway_key)],
)
async def create_draft(
    body: CreateDraftRequest,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> CreateDraftResponse:
    """Create a new post draft on Substack."""
    draft = await client.create_draft(
        title=body.title,
        subtitle=body.subtitle,
        body=body.body,
    )
    return CreateDraftResponse.from_substack(draft)
