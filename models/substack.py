from __future__ import annotations

from pydantic import BaseModel


class HandleOption(BaseModel):
    id: str | None = None
    handle: str
    type: str | None = None


class HandleOptionsResponse(BaseModel):
    potentialHandles: list[HandleOption]


class SubstackPublicProfile(BaseModel):
    id: int
    name: str
    handle: str
    previous_name: str | None = None
    photo_url: str | None = None
    bio: str | None = None
    profile_set_up_at: str | None = None
    reader_installed_at: str | None = None
    tos_accepted_at: str | None = None
    profile_disabled: bool | None = None
