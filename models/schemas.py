from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class HealthResponse(BaseModel):
    connected: bool


class ProfileResponse(BaseModel):
    id: int
    slug: str
    handle: str
    name: str
    url: str
    avatar_url: str
    bio: str | None = None

    @classmethod
    def from_raw(cls, data: dict[str, Any]) -> ProfileResponse:
        handle = data.get("handle", "")
        return cls(
            id=data["id"],
            slug=handle,
            handle=handle,
            name=data.get("name", ""),
            url=f"https://substack.com/@{handle}",
            avatar_url=data.get("photo_url", ""),
            bio=data.get("bio"),
        )


class ErrorResponse(BaseModel):
    error: str
    message: str
    status: int
