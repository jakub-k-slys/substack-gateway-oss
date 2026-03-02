from __future__ import annotations

from gateway.client.base import SubstackHTTPBase
from gateway.services.drafts import DraftsMixin
from gateway.services.following import FollowingMixin
from gateway.services.notes import NotesMixin
from gateway.services.posts import PostsMixin
from gateway.services.profiles import ProfilesMixin


class SubstackClient(
    ProfilesMixin,
    NotesMixin,
    PostsMixin,
    DraftsMixin,
    FollowingMixin,
    SubstackHTTPBase,
):
    """Async Substack API client.

    Composes service mixins for profiles, notes, posts, drafts, and following
    on top of the shared HTTP base.  Use as an async context manager::

        async with SubstackClient(
            substack_sid=...,
            connect_sid=...,
            publication_url=...,
        ) as client:
            profile = await client.get_own_profile()
    """
