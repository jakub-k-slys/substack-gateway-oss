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


# ------------------------------------------------------------------
# Notes
# ------------------------------------------------------------------


class SubstackNoteUser(BaseModel):
    id: int
    name: str
    handle: str
    photo_url: str


class SubstackNoteContext(BaseModel):
    timestamp: str
    users: list[SubstackNoteUser]


class SubstackNoteComment(BaseModel):
    id: int
    body: str
    reaction_count: int | None = None


class SubstackNote(BaseModel):
    entity_key: str
    context: SubstackNoteContext
    comment: SubstackNoteComment | None = None
    parentComments: list[SubstackNoteComment] = []


class SubstackNotesPage(BaseModel):
    items: list[SubstackNote] = []
    nextCursor: str | None = None


# ------------------------------------------------------------------
# Posts
# ------------------------------------------------------------------


class SubstackPreviewPost(BaseModel):
    id: int
    title: str
    post_date: str
    subtitle: str | None = None
    truncated_body_text: str | None = None


class SubstackFullPost(BaseModel):
    id: int
    title: str
    slug: str
    post_date: str
    canonical_url: str
    subtitle: str | None = None
    truncated_body_text: str | None = None
    body_html: str | None = None
    htmlBody: str | None = None
    reactions: dict[str, int] | None = None
    restacks: int | None = None
    postTags: list[str] | None = None
    cover_image: str | None = None


# ------------------------------------------------------------------
# Comments
# ------------------------------------------------------------------


class SubstackComment(BaseModel):
    id: int
    body: str
    author_is_admin: bool | None = None


class SubstackCommentsResponse(BaseModel):
    comments: list[SubstackComment] = []
