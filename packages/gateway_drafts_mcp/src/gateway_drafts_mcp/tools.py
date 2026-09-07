from __future__ import annotations

import base64
from typing import Any

from gateway_drafts.image import ImagesService, data_uri
from gateway_drafts.schemas import (
    AiDetectionResponse,
    CreateDraftResponse,
    DraftResponse,
    DraftsListResponse,
    PrepublishResponse,
    ScheduleDraftResponse,
)
from gateway_drafts.service import DraftsService
from gateway_mcp_common.clients import _authenticated_clients


async def list_drafts(
    token: str,
    next: str | None = None,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        drafts, next_cursor = await DraftsService(publication, substack).list_drafts(
            cursor=next
        )
    return DraftsListResponse.from_substack(
        drafts, next_cursor=next_cursor
    ).model_dump()


async def get_draft(
    draft_id: int,
    token: str,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        draft = await DraftsService(publication, substack).get_draft(draft_id)
    return DraftResponse.from_substack(draft).model_dump()


async def create_draft(
    token: str,
    title: str | None = None,
    subtitle: str | None = None,
    body: str | None = None,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        draft = await DraftsService(publication, substack).create_draft(
            title=title,
            subtitle=subtitle,
            body=body,
        )
    return CreateDraftResponse.from_substack(draft).model_dump()


async def update_draft(
    draft_id: int,
    token: str,
    title: str | None = None,
    subtitle: str | None = None,
    body: str | None = None,
) -> dict[str, Any]:
    updates: dict[str, str | None] = {}
    if title is not None:
        updates["title"] = title
    if subtitle is not None:
        updates["subtitle"] = subtitle
    if body is not None:
        updates["body"] = body
    async with _authenticated_clients(token) as (publication, substack):
        draft = await DraftsService(publication, substack).update_draft(
            draft_id, updates
        )
    return DraftResponse.from_substack(draft).model_dump()


async def delete_draft(
    draft_id: int,
    token: str,
) -> str:
    async with _authenticated_clients(token) as (publication, substack):
        await DraftsService(publication, substack).delete_draft(draft_id)
    return f"Draft {draft_id} deleted successfully."


async def get_ai_detection(
    draft_id: int,
    token: str,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        result = await DraftsService(publication, substack).ai_detection(draft_id)
    return AiDetectionResponse.from_substack(result).model_dump()


async def check_draft(
    draft_id: int,
    token: str,
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        result = await DraftsService(publication, substack).prepublish_draft(draft_id)
    return PrepublishResponse.from_substack(result).model_dump()


async def schedule_draft(
    draft_id: int,
    scheduled_at: str,
    token: str,
    post_audience: str = "only_paid",
    email_audience: str = "only_paid",
) -> dict[str, Any]:
    async with _authenticated_clients(token) as (publication, substack):
        release = await DraftsService(publication, substack).schedule_draft(
            draft_id,
            scheduled_at,
            post_audience=post_audience,
            email_audience=email_audience,
        )
    return ScheduleDraftResponse.from_substack(release).model_dump()


async def unschedule_draft(
    draft_id: int,
    token: str,
) -> str:
    async with _authenticated_clients(token) as (publication, substack):
        await DraftsService(publication, substack).unschedule_draft(draft_id)
    return f"Draft {draft_id} unscheduled successfully."


async def upload_image(
    token: str,
    image_base64: str,
    content_type: str = "image/png",
) -> dict[str, Any]:
    image = data_uri(content_type, base64.b64decode(image_base64))
    async with _authenticated_clients(token) as (publication, _substack):
        result = await ImagesService(publication).upload(image)
    return result.model_dump()
