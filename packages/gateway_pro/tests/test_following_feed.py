from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from gateway_oss.models.substack import SubstackFollowingUser
from gateway_pro.services.following_feed import FollowingFeedService
from gateway_pro.services.profile_feed import AtomFeedAuthor, AtomFeedEntriesPage


@pytest.mark.anyio
async def test_get_following_feed_page_merges_entries_from_followed_profiles() -> None:
    following = AsyncMock()
    following.get_own_following.return_value = [
        SubstackFollowingUser(id=1, handle="alice"),
        SubstackFollowingUser(id=2, handle="bob"),
    ]
    profile_feed = AsyncMock()
    profile_feed.get_entries_for_profile.side_effect = [
        AtomFeedEntriesPage(
            entries=[
                profile_feed_entry(
                    entry_id="tag:substack-gateway,post:1",
                    updated_at="2024-01-02T10:00:00.000Z",
                    author_handle="alice",
                )
            ],
            next_notes_cursor=None,
            next_posts_cursor=None,
        ),
        AtomFeedEntriesPage(
            entries=[
                profile_feed_entry(
                    entry_id="tag:substack-gateway,note:2",
                    updated_at="2024-01-03T10:00:00.000Z",
                    author_handle="bob",
                )
            ],
            next_notes_cursor=None,
            next_posts_cursor=None,
        ),
    ]
    service = FollowingFeedService(following, profile_feed)

    page = await service.get_feed_page(
        feed_type="mixed",
        limit=10,
        feed_url="https://gateway.example/api/v1/me/following/feed",
    )

    assert [entry.entry_id for entry in page.entries] == [
        "tag:substack-gateway,note:2",
        "tag:substack-gateway,post:1",
    ]
    assert [entry.author.handle for entry in page.entries] == ["bob", "alice"]
    assert page.self_url == (
        "https://gateway.example/api/v1/me/following/feed?limit=10&type=mixed"
    )
    assert page.next_url is None
    assert page.title == "Following on Substack"
    assert profile_feed.get_entries_for_profile.await_args_list[0].kwargs[
        "fallback_author"
    ] == AtomFeedAuthor(name="alice", handle="alice", avatar_url="")
    assert profile_feed.get_entries_for_profile.await_args_list[1].kwargs[
        "fallback_author"
    ] == AtomFeedAuthor(name="bob", handle="bob", avatar_url="")


def profile_feed_entry(
    *,
    entry_id: str,
    updated_at: str,
    author_handle: str,
):
    from gateway_pro.services.profile_feed import AtomFeedEntry

    return AtomFeedEntry(
        entry_id=entry_id,
        title=entry_id,
        url=f"https://substack.com/@{author_handle}",
        published_at=updated_at,
        updated_at=updated_at,
        summary=None,
        content_html=None,
        author=AtomFeedAuthor(
            name=author_handle,
            handle=author_handle,
            avatar_url="",
        ),
    )
