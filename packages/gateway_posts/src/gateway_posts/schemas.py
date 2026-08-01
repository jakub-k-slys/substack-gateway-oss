from __future__ import annotations

from pydantic import BaseModel

from gateway_core.converters.markdown import html_to_markdown
from gateway_core.models.substack import (
    SubstackFullPost,
    SubstackPreviewPost,
    SubstackProfilePostsPage,
)

# ------------------------------------------------------------------
# Posts
# ------------------------------------------------------------------


class PostResponse(BaseModel):
    id: int
    title: str
    subtitle: str | None = None
    truncated_body: str | None = None
    published_at: str

    @classmethod
    def from_substack(cls, post: SubstackPreviewPost) -> PostResponse:
        return cls(
            id=post.id,
            title=post.title,
            subtitle=post.subtitle,
            truncated_body=post.truncated_body_text,
            published_at=post.post_date,
        )


class PostsPageResponse(BaseModel):
    items: list[PostResponse]
    next: str | None = None

    @classmethod
    def from_substack(cls, page: SubstackProfilePostsPage) -> PostsPageResponse:
        return cls(
            items=[PostResponse.from_substack(p) for p in page.posts],
            next=page.next_cursor,
        )


# ------------------------------------------------------------------
# Full post
# ------------------------------------------------------------------


class FullPostResponse(BaseModel):
    id: int
    title: str
    slug: str
    subtitle: str | None = None
    url: str
    published_at: str
    html_body: str | None = None
    markdown: str | None = None
    truncated_body: str | None = None
    reactions: dict[str, int] | None = None
    restacks: int | None = None
    tags: list[str] | None = None
    cover_image: str | None = None

    @classmethod
    def from_substack(cls, post: SubstackFullPost) -> FullPostResponse:
        raw_html = post.body_html or post.html_body
        return cls(
            id=post.id,
            title=post.title,
            slug=post.slug,
            subtitle=post.subtitle,
            url=post.canonical_url,
            published_at=post.post_date,
            html_body=raw_html,
            markdown=html_to_markdown(raw_html) if raw_html else None,
            truncated_body=post.truncated_body_text,
            reactions=post.reactions,
            restacks=post.restacks,
            tags=[t.name for t in post.post_tags] if post.post_tags else None,
            cover_image=post.cover_image,
        )
