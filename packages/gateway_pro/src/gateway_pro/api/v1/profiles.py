from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, Request, Response
from gateway_oss.api.deps import get_credentials

from gateway_pro.api.deps import get_profile_feed_service
from gateway_pro.renderers.atom import render_atom_feed
from gateway_pro.services.profile_feed import ProfileFeedService

router = APIRouter(tags=["profiles"])


@router.get(
    "/profiles/{slug}/feed",
    dependencies=[Depends(get_credentials)],
)
async def get_profile_feed(
    request: Request,
    slug: str,
    service: Annotated[ProfileFeedService, Depends(get_profile_feed_service)],
    type: Annotated[Literal["mixed", "post", "note"], Query()] = "mixed",
    notes_cursor: Annotated[str | None, Query()] = None,
    posts_cursor: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(gt=0, le=100)] = 50,
) -> Response:
    page = await service.get_feed_page(
        slug,
        feed_type=type,
        notes_cursor=notes_cursor,
        posts_cursor=posts_cursor,
        limit=limit,
        feed_url=str(request.url.replace(query=None)),
    )
    return Response(
        content=render_atom_feed(page),
        media_type="application/atom+xml; charset=utf-8",
    )
