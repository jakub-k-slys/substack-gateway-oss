from __future__ import annotations

from pydantic import BaseModel

from gateway_core.models.substack import SubstackPublicProfile


class ProfileResponse(BaseModel):
    id: int
    handle: str
    name: str
    url: str
    avatar_url: str
    bio: str | None = None

    @classmethod
    def from_substack(cls, profile: SubstackPublicProfile) -> ProfileResponse:
        return cls(
            id=profile.id,
            handle=profile.handle,
            name=profile.name,
            url=f"https://substack.com/@{profile.handle}",
            avatar_url=profile.photo_url or "",
            bio=profile.bio,
        )
