from __future__ import annotations

from pydantic import BaseModel

from models.substack import SubstackPublicProfile


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
    def from_substack(cls, profile: SubstackPublicProfile) -> ProfileResponse:
        return cls(
            id=profile.id,
            slug=profile.handle,
            handle=profile.handle,
            name=profile.name,
            url=f"https://substack.com/@{profile.handle}",
            avatar_url=profile.photo_url or "",
            bio=profile.bio,
        )


class ErrorResponse(BaseModel):
    error: str
    message: str
    status: int
