from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Path, Query, UploadFile

from gateway_drafts._cursor import InvalidCursorError
from gateway_drafts.image import ImagesService, data_uri
from gateway_drafts.schemas import (
    AiDetectionResponse,
    CreateDraftRequest,
    CreateDraftResponse,
    DraftResponse,
    DraftsListResponse,
    ImageUploadResult,
    PrepublishResponse,
    ScheduleDraftRequest,
    ScheduleDraftResponse,
    UpdateDraftRequest,
)
from gateway_drafts.service import DraftsService
from gateway_drafts_rest.deps import get_drafts_service, get_images_service
from gateway_rest_common.deps import get_credentials

router = APIRouter(tags=["drafts"])


@router.get(
    "/drafts",
    response_model=DraftsListResponse,
    dependencies=[Depends(get_credentials)],
)
async def list_drafts(
    service: Annotated[DraftsService, Depends(get_drafts_service)],
    next: Annotated[
        str | None, Query(description="Opaque cursor from a previous response.")
    ] = None,
) -> DraftsListResponse:
    """List post drafts, newest first, in pages of 10 with cursor-based pagination."""
    try:
        drafts, next_cursor = await service.list_drafts(cursor=next)
    except InvalidCursorError as exc:
        raise HTTPException(status_code=400, detail="Invalid cursor") from exc
    return DraftsListResponse.from_substack(drafts, next_cursor=next_cursor)


@router.get(
    "/drafts/{draft_id}",
    response_model=DraftResponse,
    dependencies=[Depends(get_credentials)],
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
    dependencies=[Depends(get_credentials)],
)
async def update_draft(
    draft_id: Annotated[int, Path(gt=0)],
    body: UpdateDraftRequest,
    service: Annotated[DraftsService, Depends(get_drafts_service)],
) -> DraftResponse:
    """Update specific fields of a Substack post draft."""
    draft = await service.update_draft(draft_id, body.provided_updates())
    return DraftResponse.from_substack(draft)


@router.delete(
    "/drafts/{draft_id}",
    status_code=204,
    dependencies=[Depends(get_credentials)],
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
    dependencies=[Depends(get_credentials)],
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


@router.get(
    "/drafts/{draft_id}/ai-detection",
    response_model=AiDetectionResponse,
    dependencies=[Depends(get_credentials)],
)
async def ai_detection(
    draft_id: Annotated[int, Path(gt=0)],
    service: Annotated[DraftsService, Depends(get_drafts_service)],
) -> AiDetectionResponse:
    """Run Substack's Pangram AI-writing detection on a draft."""
    return AiDetectionResponse.from_substack(await service.ai_detection(draft_id))


@router.get(
    "/drafts/{draft_id}/prepublish",
    response_model=PrepublishResponse,
    dependencies=[Depends(get_credentials)],
)
async def prepublish_draft(
    draft_id: Annotated[int, Path(gt=0)],
    service: Annotated[DraftsService, Depends(get_drafts_service)],
) -> PrepublishResponse:
    """Run Substack's pre-publish validation on a draft."""
    return PrepublishResponse.from_substack(await service.prepublish_draft(draft_id))


@router.post(
    "/drafts/{draft_id}/schedule",
    response_model=ScheduleDraftResponse,
    dependencies=[Depends(get_credentials)],
)
async def schedule_draft(
    draft_id: Annotated[int, Path(gt=0)],
    body: ScheduleDraftRequest,
    service: Annotated[DraftsService, Depends(get_drafts_service)],
) -> ScheduleDraftResponse:
    """Schedule a draft for timed release."""
    release = await service.schedule_draft(
        draft_id,
        body.scheduled_at,
        post_audience=body.post_audience or "only_paid",
        email_audience=body.email_audience or "only_paid",
    )
    return ScheduleDraftResponse.from_substack(release)


@router.delete(
    "/drafts/{draft_id}/schedule",
    status_code=204,
    dependencies=[Depends(get_credentials)],
)
async def unschedule_draft(
    draft_id: Annotated[int, Path(gt=0)],
    service: Annotated[DraftsService, Depends(get_drafts_service)],
) -> None:
    """Cancel a draft's scheduled release."""
    await service.unschedule_draft(draft_id)


@router.post(
    "/images",
    response_model=ImageUploadResult,
    status_code=201,
    dependencies=[Depends(get_credentials)],
    tags=["images"],
)
async def upload_image(
    file: Annotated[UploadFile, File()],
    service: Annotated[ImagesService, Depends(get_images_service)],
) -> ImageUploadResult:
    """Upload an image file to Substack and return its hosted URL and dimensions."""
    raw = await file.read()
    content_type = file.content_type or "application/octet-stream"
    return await service.upload(data_uri(content_type, raw))
