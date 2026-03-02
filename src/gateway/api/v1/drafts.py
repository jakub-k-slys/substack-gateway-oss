from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path

from gateway.api.deps import get_substack_client, require_gateway_key
from gateway.client.substack import SubstackClient
from gateway.models.schemas import (
    CreateDraftRequest,
    CreateDraftResponse,
    DraftResponse,
    DraftsListResponse,
    UpdateDraftRequest,
)

router = APIRouter(tags=["drafts"])


@router.get(
    "/drafts",
    response_model=DraftsListResponse,
    dependencies=[Depends(require_gateway_key)],
)
async def list_drafts(
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> DraftsListResponse:
    """List all post drafts on Substack."""
    drafts = await client.list_drafts()
    return DraftsListResponse.from_substack(drafts)


@router.get(
    "/drafts/{draft_id}",
    response_model=DraftResponse,
    dependencies=[Depends(require_gateway_key)],
)
async def get_draft(
    draft_id: Annotated[int, Path(gt=0)],
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> DraftResponse:
    """Fetch a post draft from Substack by ID."""
    draft = await client.get_draft(draft_id)
    return DraftResponse.from_substack(draft)


@router.put(
    "/drafts/{draft_id}",
    response_model=DraftResponse,
    dependencies=[Depends(require_gateway_key)],
)
async def update_draft(
    draft_id: Annotated[int, Path(gt=0)],
    body: UpdateDraftRequest,
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> DraftResponse:
    """Update specific fields of a Substack post draft."""
    draft = await client.update_draft(draft_id, body.to_substack_payload())
    return DraftResponse.from_substack(draft)


@router.delete(
    "/drafts/{draft_id}",
    status_code=204,
    dependencies=[Depends(require_gateway_key)],
)
async def delete_draft(
    draft_id: Annotated[int, Path(gt=0)],
    client: Annotated[SubstackClient, Depends(get_substack_client)],
) -> None:
    """Delete a post draft on Substack."""
    await client.delete_draft(draft_id)


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
