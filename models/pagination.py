from __future__ import annotations

from pydantic import BaseModel, Field


class OffsetPage(BaseModel):
    """Shared dependency for limit/offset paginated endpoints."""

    limit: int = Field(default=25, gt=0, le=100)
    offset: int = Field(default=0, ge=0)


class CursorPage(BaseModel):
    """Shared dependency for cursor-paginated endpoints."""

    cursor: str | None = None
