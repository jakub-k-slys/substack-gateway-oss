from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, Request, Response
from gateway_oss.api.deps import get_credentials

from gateway_pro.api.deps import get_following_feed_service
from gateway_pro.renderers.atom import render_atom_feed
from gateway_pro.services.following_feed import FollowingFeedService

router = APIRouter(tags=["me"])


@router.get(
    "/me/following/feed",
    dependencies=[Depends(get_credentials)],
)
async def get_me_following_feed(
    request: Request,
    service: Annotated[FollowingFeedService, Depends(get_following_feed_service)],
    type: Annotated[Literal["mixed", "post", "note"], Query()] = "mixed",
    limit: Annotated[int, Query(gt=0, le=100)] = 10,
    total: Annotated[int | None, Query(gt=0)] = None,
) -> Response:
    page = await service.get_feed_page(
        feed_type=type,
        limit=limit,
        total=total,
        feed_url=str(request.url.replace(query=None)),
    )
    return Response(
        content=render_atom_feed(page),
        media_type="application/atom+xml; charset=utf-8",
    )
