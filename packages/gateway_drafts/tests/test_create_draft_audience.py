import asyncio

import pytest
from pydantic import ValidationError

from gateway_drafts.schemas import CreateDraftRequest
from gateway_drafts.service import DraftsService


class _Resp:
    def json(self):
        return {"id": 1, "uuid": "u"}


class _Pub:
    def __init__(self):
        self.sent = None

    async def post(self, path, json):
        self.sent = json
        return _Resp()


class _Sub:
    async def get_own_id(self):
        return 7


def _create(**kw):
    pub = _Pub()
    asyncio.run(DraftsService(pub, _Sub()).create_draft(title="t", **kw))
    return pub.sent["audience"]


def test_new_draft_defaults_to_everyone():
    assert _create() == "everyone"
    assert CreateDraftRequest().audience == "everyone"


def test_audience_is_passed_through_and_validated():
    assert _create(audience="only_paid") == "only_paid"
    with pytest.raises(ValidationError):
        CreateDraftRequest(audience="nobody")
