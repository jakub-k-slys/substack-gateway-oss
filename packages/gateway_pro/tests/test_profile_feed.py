from __future__ import annotations

from gateway_pro.renderers.atom import render_atom_feed
from gateway_pro.services.profile_feed import (
    AtomFeedAuthor,
    AtomFeedEntry,
    AtomFeedPage,
)


def test_render_atom_feed_includes_next_link_and_escaped_content() -> None:
    page = AtomFeedPage(
        feed_id="tag:substack-gateway,profile:1",
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
                entry_id="tag:substack-gateway,note:1",
                title="Note by Example Author",
                url="https://substack.com/@example",
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
        feed_id="tag:substack-gateway,profile:1",
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
        feed_id="tag:substack-gateway,profile:1",
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
