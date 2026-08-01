from __future__ import annotations

from pydantic import BaseModel

from gateway_core.models.substack import SubstackFollowingUser


class FollowingUserResponse(BaseModel):
    id: int
    handle: str

    @classmethod
    def from_substack(cls, user: SubstackFollowingUser) -> FollowingUserResponse:
        return cls(id=user.id, handle=user.handle)


class FollowingResponse(BaseModel):
    items: list[FollowingUserResponse]

    @classmethod
    def from_substack(cls, users: list[SubstackFollowingUser]) -> FollowingResponse:
        return cls(items=[FollowingUserResponse.from_substack(u) for u in users])
