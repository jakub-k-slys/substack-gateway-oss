from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path

from gateway.api.deps import get_drafts_service, require_gateway_key
from gateway.models.schemas import (
    CreateDraftRequest,
    CreateDraftResponse,
    DraftResponse,
    DraftsListResponse,
    UpdateDraftRequest,
)
from gateway.services.drafts import DraftsService

router = APIRouter(tags=["drafts"])


@router.get(
    "/drafts",
    response_model=DraftsListResponse,
    dependencies=[Depends(require_gateway_key)],
)
async def list_drafts(
    service: Annotated[DraftsService, Depends(get_drafts_service)],
) -> DraftsListResponse:
    """List all post drafts on Substack."""
    drafts = await service.list_drafts()
    return DraftsListResponse.from_substack(drafts)


@router.get(
    "/drafts/{draft_id}",
    response_model=DraftResponse,
    dependencies=[Depends(require_gateway_key)],
)
async def get_draft(
    draft_id: Annotated[int, Path(gt=0)],
    service: Annotated[DraftsService, Depends(get_drafts_service)],
) -> DraftResponse:
    """Fetch a post draft from Substack by ID."""
    draft = await service.get_draft(draft_id)
    return DraftResponse.from_substack(draft)


@router.put(
    "/drafts/{draft_id}",
    response_model=DraftResponse,
    dependencies=[Depends(require_gateway_key)],
)
async def update_draft(
    draft_id: Annotated[int, Path(gt=0)],
    body: UpdateDraftRequest,
    service: Annotated[DraftsService, Depends(get_drafts_service)],
) -> DraftResponse:
    """Update specific fields of a Substack post draft."""
    draft = await service.update_draft(draft_id, body.to_substack_payload())
    return DraftResponse.from_substack(draft)


@router.delete(
    "/drafts/{draft_id}",
    status_code=204,
    dependencies=[Depends(require_gateway_key)],
)
async def delete_draft(
    draft_id: Annotated[int, Path(gt=0)],
    service: Annotated[DraftsService, Depends(get_drafts_service)],
) -> None:
    """Delete a post draft on Substack."""
    await service.delete_draft(draft_id)


@router.post(
    "/drafts",
    response_model=CreateDraftResponse,
    status_code=201,
    dependencies=[Depends(require_gateway_key)],
)
async def create_draft(
    body: CreateDraftRequest,
    service: Annotated[DraftsService, Depends(get_drafts_service)],
) -> CreateDraftResponse:
    """Create a new post draft on Substack."""
    draft = await service.create_draft(
        title=body.title,
        subtitle=body.subtitle,
        body=body.body,
    )
    return CreateDraftResponse.from_substack(draft)
