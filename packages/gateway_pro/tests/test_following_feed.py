from __future__ import annotations

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from gateway_oss.models.substack import SubstackFollowingUser
from gateway_pro.services.following_feed import FollowingFeedService
from gateway_pro.services.profile_feed import AtomFeedAuthor, AtomFeedEntriesPage


@pytest.fixture(autouse=True)
async def clear_following_feed_cache() -> AsyncGenerator[None]:
    await FollowingFeedService._get_followed_profile_entries.cache.clear()
    yield
    await FollowingFeedService._get_followed_profile_entries.cache.clear()


@pytest.mark.anyio
async def test_get_following_feed_page_merges_entries_from_followed_profiles() -> None:
    following = AsyncMock()
    following.get_own_following.return_value = [
        SubstackFollowingUser(id=1, handle="alice"),
        SubstackFollowingUser(id=2, handle="bob"),
    ]
    profile_feed = AsyncMock()
    profile_feed.get_entries_for_profile_best_effort.side_effect = [
        AtomFeedEntriesPage(
            entries=[
                profile_feed_entry(
                    entry_id="post:1",
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
                    entry_id="note:2",
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
        "note:2",
        "post:1",
    ]
    assert [entry.author.handle for entry in page.entries] == ["bob", "alice"]
    assert page.self_url == (
        "https://gateway.example/api/v1/me/following/feed?limit=10&type=mixed"
    )
    assert page.next_url is None
    assert page.title == "Following on Substack"
    assert (
        profile_feed.get_entries_for_profile_best_effort.await_args_list[0].kwargs[
            "limit"
        ]
        == 10
    )
    assert profile_feed.get_entries_for_profile_best_effort.await_args_list[0].kwargs[
        "fallback_author"
    ] == AtomFeedAuthor(name="alice", handle="alice", avatar_url="")
    assert profile_feed.get_entries_for_profile_best_effort.await_args_list[1].kwargs[
        "fallback_author"
    ] == AtomFeedAuthor(name="bob", handle="bob", avatar_url="")


@pytest.mark.anyio
async def test_get_following_feed_page_reuses_cached_profile_entries() -> None:
    following = AsyncMock()
    following.get_own_following.return_value = [
        SubstackFollowingUser(id=1, handle="alice"),
    ]
    profile_feed = AsyncMock()
    profile_feed.get_entries_for_profile_best_effort.return_value = AtomFeedEntriesPage(
        entries=[
            profile_feed_entry(
                entry_id="post:1",
                updated_at="2024-01-02T10:00:00.000Z",
                author_handle="alice",
            )
        ],
        next_notes_cursor=None,
        next_posts_cursor=None,
    )
    service = FollowingFeedService(following, profile_feed)

    first_page = await service.get_feed_page(
        feed_type="mixed",
        limit=10,
        feed_url="https://gateway.example/api/v1/me/following/feed",
    )
    second_page = await service.get_feed_page(
        feed_type="mixed",
        limit=10,
        feed_url="https://gateway.example/api/v1/me/following/feed",
    )

    assert [entry.entry_id for entry in first_page.entries] == ["post:1"]
    assert [entry.entry_id for entry in second_page.entries] == ["post:1"]
    assert profile_feed.get_entries_for_profile_best_effort.await_count == 1


@pytest.mark.anyio
async def test_get_following_feed_page_logs_cache_hit(
    caplog: pytest.LogCaptureFixture,
) -> None:
    following = AsyncMock()
    following.get_own_following.return_value = [
        SubstackFollowingUser(id=1, handle="alice"),
    ]
    profile_feed = AsyncMock()
    profile_feed.get_entries_for_profile_best_effort.return_value = AtomFeedEntriesPage(
        entries=[
            profile_feed_entry(
                entry_id="post:1",
                updated_at="2024-01-02T10:00:00.000Z",
                author_handle="alice",
            )
        ],
        next_notes_cursor=None,
        next_posts_cursor=None,
    )
    service = FollowingFeedService(following, profile_feed)
    caplog.set_level("DEBUG")

    await service.get_feed_page(
        feed_type="mixed",
        limit=10,
        feed_url="https://gateway.example/api/v1/me/following/feed",
    )
    await service.get_feed_page(
        feed_type="mixed",
        limit=10,
        feed_url="https://gateway.example/api/v1/me/following/feed",
    )

    assert "Following Feed cache miss for profile_id=1 handle=alice" in caplog.text
    assert "Following Feed cache hit for profile_id=1 handle=alice" in caplog.text


@pytest.mark.anyio
async def test_get_following_feed_page_applies_total_limit_after_sorting() -> None:
    following = AsyncMock()
    following.get_own_following.return_value = [
        SubstackFollowingUser(id=1, handle="alice"),
        SubstackFollowingUser(id=2, handle="bob"),
    ]
    profile_feed = AsyncMock()
    profile_feed.get_entries_for_profile_best_effort.side_effect = [
        AtomFeedEntriesPage(
            entries=[
                profile_feed_entry(
                    entry_id="post:1",
                    updated_at="2024-01-02T10:00:00.000Z",
                    author_handle="alice",
                ),
                profile_feed_entry(
                    entry_id="post:2",
                    updated_at="2024-01-04T10:00:00.000Z",
                    author_handle="alice",
                ),
            ],
            next_notes_cursor=None,
            next_posts_cursor=None,
        ),
        AtomFeedEntriesPage(
            entries=[
                profile_feed_entry(
                    entry_id="note:3",
                    updated_at="2024-01-03T10:00:00.000Z",
                    author_handle="bob",
                ),
                profile_feed_entry(
                    entry_id="note:4",
                    updated_at="2024-01-05T10:00:00.000Z",
                    author_handle="bob",
                ),
            ],
            next_notes_cursor=None,
            next_posts_cursor=None,
        ),
    ]
    service = FollowingFeedService(following, profile_feed)

    page = await service.get_feed_page(
        feed_type="mixed",
        limit=10,
        total=3,
        feed_url="https://gateway.example/api/v1/me/following/feed",
    )

    assert [entry.entry_id for entry in page.entries] == [
        "note:4",
        "post:2",
        "note:3",
    ]
    assert page.self_url == (
        "https://gateway.example/api/v1/me/following/feed?limit=10&type=mixed&total=3"
    )


@pytest.mark.anyio
async def test_get_following_feed_page_keeps_other_profiles_when_one_profile_fails() -> (
    None
):
    following = AsyncMock()
    following.get_own_following.return_value = [
        SubstackFollowingUser(id=1, handle="alice"),
        SubstackFollowingUser(id=2, handle="bob"),
    ]
    profile_feed = AsyncMock()
    profile_feed.get_entries_for_profile_best_effort.side_effect = [
        AtomFeedEntriesPage(
            entries=[
                profile_feed_entry(
                    entry_id="post:1",
                    updated_at="2024-01-02T10:00:00.000Z",
                    author_handle="alice",
                )
            ],
            next_notes_cursor=None,
            next_posts_cursor=None,
        ),
        AtomFeedEntriesPage(
            entries=[],
            next_notes_cursor=None,
            next_posts_cursor=None,
            partial=True,
        ),
    ]
    service = FollowingFeedService(following, profile_feed)

    page = await service.get_feed_page(
        feed_type="mixed",
        limit=10,
        feed_url="https://gateway.example/api/v1/me/following/feed",
    )

    assert [entry.entry_id for entry in page.entries] == ["post:1"]
    assert page.partial is True


@pytest.mark.anyio
async def test_get_following_feed_page_is_not_partial_when_all_profiles_succeed() -> (
    None
):
    following = AsyncMock()
    following.get_own_following.return_value = [
        SubstackFollowingUser(id=1, handle="alice"),
    ]
    profile_feed = AsyncMock()
    profile_feed.get_entries_for_profile_best_effort.return_value = AtomFeedEntriesPage(
        entries=[
            profile_feed_entry(
                entry_id="post:1",
                updated_at="2024-01-02T10:00:00.000Z",
                author_handle="alice",
            )
        ],
        next_notes_cursor=None,
        next_posts_cursor=None,
        partial=False,
    )
    service = FollowingFeedService(following, profile_feed)

    page = await service.get_feed_page(
        feed_type="mixed",
        limit=10,
        feed_url="https://gateway.example/api/v1/me/following/feed",
    )

    assert page.partial is False


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
