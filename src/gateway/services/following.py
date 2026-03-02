from __future__ import annotations

import logging

from gateway.client.publication import PublicationClient
from gateway.client.substack import SubstackClient
from gateway.models.substack import SubstackFollowingUser, SubstackSubscriberLists

_log = logging.getLogger(__name__)


class FollowingService:
    def __init__(self, pub: PublicationClient, sub: SubstackClient) -> None:
        self._pub = pub
        self._sub = sub

    async def get_own_following(self) -> list[SubstackFollowingUser]:
        """GET /user/{id}/subscriber-lists — users the caller follows."""
        _log.debug("Fetching own following list")
        user_id = await self._sub.get_own_id()
        r = await self._pub._request(
            "GET",
            f"{self._pub._base}/user/{user_id}/subscriber-lists",
            params={"lists": "following"},
        )
        data = SubstackSubscriberLists.model_validate(r.json())
        users: list[SubstackFollowingUser] = []
        for sl in data.subscriber_lists:
            for group in sl.groups:
                users.extend(group.users)
        _log.debug("Got %d following users for user_id=%d", len(users), user_id)
        return users
