from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from gateway_drafts.schemas import CreateDraftRequest
from gateway_drafts.service import DraftsService


class _Resp:
    def json(self) -> object:
        return {"id": 1, "uuid": "u"}


async def _create(**kw: Any) -> str:
    pub = AsyncMock()
    pub.post.return_value = _Resp()
    sub = AsyncMock()
    sub.get_own_id.return_value = 7
    await DraftsService(pub, sub).create_draft(title="t", **kw)
    return pub.post.await_args.kwargs["json"]["audience"]


@pytest.mark.anyio
async def test_new_draft_defaults_to_everyone() -> None:
    assert await _create() == "everyone"
    assert CreateDraftRequest().audience == "everyone"


@pytest.mark.anyio
async def test_audience_is_passed_through_and_validated() -> None:
    assert await _create(audience="only_paid") == "only_paid"
    with pytest.raises(ValidationError):
        CreateDraftRequest.model_validate({"audience": "nobody"})
