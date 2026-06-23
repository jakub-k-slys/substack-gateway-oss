from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class HandleOption(BaseModel):
    id: str | None = None
    handle: str
    type: str | None = None


class HandleOptionsResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    potential_handles: list[HandleOption]


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


class SubstackPreviewPost(BaseModel):
    id: int
    title: str
    post_date: str
    subtitle: str | None = None
    truncated_body_text: str | None = None
    slug: str | None = None
    canonical_url: str | None = None


class SubstackFeedPublication(BaseModel):
    author_name: str | None = None
    author_handle: str | None = None
    author_photo_url: str | None = None


# ------------------------------------------------------------------
# Notes
# ------------------------------------------------------------------


class SubstackNoteUser(BaseModel):
    id: int
    name: str
    handle: str
    photo_url: str | None = None


class SubstackNoteContext(BaseModel):
    timestamp: str
    users: list[SubstackNoteUser]


class SubstackNoteComment(BaseModel):
    id: int
    body: str
    name: str | None = None
    handle: str | None = None
    photo_url: str | None = None
    reaction_count: int | None = None


class SubstackNote(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    entity_key: str
    type: str | None = None
    context: SubstackNoteContext
    publication: SubstackFeedPublication | None = None
    post: SubstackPreviewPost | None = None
    comment: SubstackNoteComment | None = None
    parent_comments: list[SubstackNoteComment] = Field(
        alias="parentComments", default=[]
    )


class SubstackNotesPage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[SubstackNote] = []
    next_cursor: str | None = Field(alias="nextCursor", default=None)


# ------------------------------------------------------------------
# Posts
# ------------------------------------------------------------------


class SubstackProfilePostsPage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    posts: list[SubstackPreviewPost] = []
    next_cursor: str | None = Field(alias="nextCursor", default=None)


class SubstackPostTag(BaseModel):
    name: str
    slug: str | None = None


class SubstackFullPost(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    title: str
    slug: str
    post_date: str
    canonical_url: str
    subtitle: str | None = None
    truncated_body_text: str | None = None
    # Substack has used both snake_case (body_html) and camelCase (htmlBody) for
    # the HTML body field across different endpoints/versions. Both are captured
    # here and merged in FullPostResponse.from_substack via `body_html or html_body`.
    body_html: str | None = None
    html_body: str | None = Field(alias="htmlBody", default=None)
    reactions: dict[str, int] | None = None
    restacks: int | None = None
    post_tags: list[SubstackPostTag] | None = Field(alias="postTags", default=None)
    cover_image: str | None = None


class SubstackPostResponse(BaseModel):
    post: SubstackFullPost


# ------------------------------------------------------------------
# Note creation
# ------------------------------------------------------------------


class SubstackNoteCreated(BaseModel):
    id: int
    date: str | None = None
    status: str | None = None


class SubstackAttachmentCreated(BaseModel):
    id: str


# ------------------------------------------------------------------
# Comments
# ------------------------------------------------------------------


class SubstackComment(BaseModel):
    id: int
    body: str
    author_is_admin: bool | None = None
    name: str | None = None
    handle: str | None = None
    user_id: int | None = None


class SubstackCommentsResponse(BaseModel):
    comments: list[SubstackComment] = []


class SubstackItemResponse(BaseModel):
    item: SubstackNote


# ------------------------------------------------------------------
# Following
# ------------------------------------------------------------------


class SubstackFollowingUser(BaseModel):
    id: int
    handle: str


class SubstackFollowingGroup(BaseModel):
    users: list[SubstackFollowingUser]


class SubstackFollowingList(BaseModel):
    id: str
    name: str
    groups: list[SubstackFollowingGroup]


class SubstackSubscriberLists(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    subscriber_lists: list[SubstackFollowingList]


# ------------------------------------------------------------------
# User settings
# ------------------------------------------------------------------


class SubstackUserSetting(BaseModel):
    user_id: int
    type: str
    value_bool: bool | None = None
    value_datetime: str | None = None
    value_integer: int | None = None
    value_text: str | None = None


class SubstackUserSettingsResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    user_settings: list[SubstackUserSetting]
    qualifies_for_badge: bool | None = None
