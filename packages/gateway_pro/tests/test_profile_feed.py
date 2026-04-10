from __future__ import annotations

from typing import cast

import pytest
from gateway_oss.client.substack import SubstackClient
from gateway_oss.models.substack import (
    SubstackFeedPublication,
    SubstackNote,
    SubstackNoteComment,
    SubstackNoteContext,
    SubstackPreviewPost,
)
from gateway_pro.renderers.atom import render_atom_feed
from gateway_pro.services.profile_feed import (
    AtomFeedAuthor,
    AtomFeedEntry,
    AtomFeedPage,
    ProfileFeedService,
    SubstackCursorPostsPage,
)


def test_render_atom_feed_includes_next_link_and_escaped_content() -> None:
    page = AtomFeedPage(
        feed_id="profile:1",
        title="Example Feed",
        subtitle="Feed subtitle",
        author=AtomFeedAuthor(
            name="Example Author",
            handle="example",
            avatar_url="https://substack.com/img/avatar.jpg",
        ),
        updated_at="2024-01-15T10:00:00.000Z",
        icon_url="https://substack.com/img/avatar.jpg",
        alternate_url="https://substack.com/@example",
        self_url="/api/v1/profiles/example/feed",
        next_url="/api/v1/profiles/example/feed?notes_cursor=abc&posts_cursor=def&limit=50",
        entries=[
            AtomFeedEntry(
                entry_id="note:1",
                title="Note by Example Author",
                url="https://substack.com/@example/note/c-1",
                published_at="2024-01-15T10:00:00.000Z",
                updated_at="2024-01-15T10:00:00.000Z",
                summary="Summary <with> chars",
                content_html="<p>Hello & welcome</p>",
                author=AtomFeedAuthor(
                    name="Example Author",
                    handle="example",
                    avatar_url="https://substack.com/img/avatar.jpg",
                ),
            )
        ],
    )

    xml = render_atom_feed(page)

    assert 'rel="next"' in xml
    assert "Summary &lt;with&gt; chars" in xml
    assert "&lt;p&gt;Hello &amp; welcome&lt;/p&gt;" in xml


def test_render_atom_feed_keeps_type_in_pagination_link() -> None:
    page = AtomFeedPage(
        feed_id="profile:1",
        title="Example Feed",
        subtitle=None,
        author=AtomFeedAuthor(
            name="Example Author",
            handle="example",
            avatar_url="https://substack.com/img/avatar.jpg",
        ),
        updated_at="2024-01-15T10:00:00.000Z",
        icon_url=None,
        alternate_url="https://substack.com/@example",
        self_url="/api/v1/profiles/example/feed?limit=50&type=note",
        next_url="/api/v1/profiles/example/feed?limit=50&type=note&notes_cursor=abc",
        entries=[],
    )

    xml = render_atom_feed(page)

    assert "type=note" in xml


def test_render_atom_feed_keeps_limit_in_pagination_link() -> None:
    page = AtomFeedPage(
        feed_id="profile:1",
        title="Example Feed",
        subtitle=None,
        author=AtomFeedAuthor(
            name="Example Author",
            handle="example",
            avatar_url="https://substack.com/img/avatar.jpg",
        ),
        updated_at="2024-01-15T10:00:00.000Z",
        icon_url=None,
        alternate_url="https://substack.com/@example",
        self_url="/api/v1/profiles/example/feed?limit=3&type=note",
        next_url="/api/v1/profiles/example/feed?limit=3&type=note&notes_cursor=abc",
        entries=[],
    )

    xml = render_atom_feed(page)

    assert "limit=3" in xml


def test_feed_item_to_entry_normalizes_note_ids_and_urls() -> None:
    service = ProfileFeedService(sub=cast(SubstackClient, object()))

    entry = service._feed_item_to_entry(
        SubstackNote(
            entity_key="c-131661687",
            type="comment",
            context=SubstackNoteContext(
                timestamp="2025-07-03T10:36:54.004Z",
                users=[],
            ),
            comment=SubstackNoteComment(
                id=131661687,
                body="Hello",
                handle="angelsant",
                name="Angel Rodriguez Santiago",
            ),
        ),
        fallback_author=AtomFeedAuthor(
            name="Fallback",
            handle="fallback",
            avatar_url="",
        ),
    )

    assert entry.entry_id == "note:131661687"
    assert entry.url == "https://substack.com/@angelsant/note/c-131661687"


def test_feed_item_to_entry_uses_post_identity_for_post_items() -> None:
    service = ProfileFeedService(sub=cast(SubstackClient, object()))

    entry = service._feed_item_to_entry(
        SubstackNote(
            entity_key="p-167278092",
            type="post",
            context=SubstackNoteContext(
                timestamp="2025-07-01T16:36:39.842Z",
                users=[],
            ),
            publication=SubstackFeedPublication(
                author_name="Jenny Ouyang",
                author_handle="jennyouyang",
                author_photo_url="https://example.com/jenny.jpg",
            ),
            post=SubstackPreviewPost(
                id=167278092,
                title="openai is coming to steal your clients",
                post_date="2025-07-01T16:36:39.842Z",
                canonical_url="https://angelsant.substack.com/p/openai-is-coming-to-steal-your-clients",
            ),
        ),
        fallback_author=AtomFeedAuthor(
            name="Angel Rodriguez Santiago",
            handle="angelsant",
            avatar_url="",
        ),
    )

    assert entry.entry_id == "post:167278092"
    assert (
        entry.url
        == "https://angelsant.substack.com/p/openai-is-coming-to-steal-your-clients"
    )
    assert entry.author == AtomFeedAuthor(
        name="Jenny Ouyang",
        handle="jennyouyang",
        avatar_url="https://example.com/jenny.jpg",
    )


@pytest.mark.anyio
async def test_get_entries_for_profile_best_effort_keeps_posts_when_notes_fail(
    caplog: pytest.LogCaptureFixture,
) -> None:
    class BestEffortTestProfileFeedService(ProfileFeedService):
        async def _get_notes_for_profile(  # type: ignore[override]
            self, profile_id: int, *, cursor: str | None
        ):
            raise RuntimeError("notes failed")

        async def _get_posts_for_profile(  # type: ignore[override]
            self, profile_id: int, *, cursor: str | None, limit: int
        ) -> SubstackCursorPostsPage:
            return SubstackCursorPostsPage(
                posts=[
                    SubstackPreviewPost(
                        id=123,
                        title="Post survives",
                        post_date="2024-01-03T10:00:00.000Z",
                        canonical_url="https://example.com/p/post-survives",
                    )
                ]
            )

    service = BestEffortTestProfileFeedService(sub=cast(SubstackClient, object()))
    caplog.set_level("WARNING")

    page = await service.get_entries_for_profile_best_effort(
        111111,
        fallback_author=AtomFeedAuthor(
            name="alice",
            handle="alice",
            avatar_url="",
        ),
        feed_type="mixed",
        limit=10,
    )

    assert [entry.entry_id for entry in page.entries] == ["post:123"]
    assert (
        "Failed to fetch notes for followed profile_id=111111 handle=alice"
        in caplog.text
    )
