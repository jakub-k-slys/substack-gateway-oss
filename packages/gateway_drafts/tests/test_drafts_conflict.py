from __future__ import annotations

import json
from typing import Any

import pytest

from gateway_drafts.converters.dialect.errors import DraftMarkdownError
from gateway_drafts.models.substack import SubstackDraft
from gateway_drafts.schemas import DraftResponse, UpdateDraftRequest
from gateway_drafts.service import DraftConflictError, DraftsService

CURRENT = "2026-03-01T09:53:35.569Z"
STALE = "2026-01-01T00:00:00.000Z"


class _Resp:
    def __init__(self, payload: object) -> None:
        self._p = payload

    def json(self) -> object:
        return self._p


class _FakePub:
    """Records calls; GET returns a draft stamped CURRENT, PUT echoes a new stamp."""

    def __init__(self) -> None:
        self.gets: list[str] = []
        self.puts: list[tuple[str, dict[str, Any]]] = []

    async def get(self, path: str, **_: Any) -> _Resp:
        self.gets.append(path)
        return _Resp({"draft_title": "old", "draft_updated_at": CURRENT})

    async def put(self, path: str, json: dict[str, Any]) -> _Resp:
        self.puts.append((path, json))
        return _Resp({**json, "draft_updated_at": "2026-03-02T00:00:00.000Z"})


def _service(pub: _FakePub) -> DraftsService:
    return DraftsService(pub, None)  # ty: ignore[invalid-argument-type]


@pytest.mark.anyio
async def test_stale_expected_updated_at_raises_and_skips_put() -> None:
    pub = _FakePub()
    with pytest.raises(DraftConflictError) as exc:
        await _service(pub).update_draft(1, {"title": "x"}, expected_updated_at=STALE)
    assert pub.puts == []
    assert pub.gets == ["drafts/1"]
    assert str(exc.value) == (
        f"Draft 1 changed since it was read (now {CURRENT}); "
        "fetch it again before updating."
    )


@pytest.mark.anyio
async def test_matching_expected_updated_at_puts() -> None:
    pub = _FakePub()
    draft = await _service(pub).update_draft(
        1, {"title": "x"}, expected_updated_at=CURRENT
    )
    assert pub.puts == [("drafts/1", {"draft_title": "x"})]
    assert draft.draft_title == "x"
    assert draft.draft_updated_at == "2026-03-02T00:00:00.000Z"


@pytest.mark.anyio
async def test_no_expected_updated_at_skips_the_get() -> None:
    pub = _FakePub()
    await _service(pub).update_draft(1, {"title": "x"})
    assert pub.gets == []
    assert len(pub.puts) == 1


@pytest.mark.anyio
async def test_malformed_body_raises_markdown_error_before_put() -> None:
    pub = _FakePub()
    with pytest.raises(DraftMarkdownError) as exc:
        await _service(pub).update_draft(
            1, {"body": "```substack-node\n{oops\n```"}, expected_updated_at=CURRENT
        )
    assert exc.value.line == 1
    assert pub.puts == []


def test_provided_updates_excludes_expected_updated_at() -> None:
    req = UpdateDraftRequest(title="t", expected_updated_at=STALE)
    assert req.expected_updated_at == STALE
    assert req.provided_updates() == {"title": "t"}
    assert json.loads(req.model_dump_json())["expected_updated_at"] == STALE


def test_draft_response_exposes_updated_at() -> None:
    resp = DraftResponse.from_substack(SubstackDraft(draft_updated_at="u"))
    assert resp.updated_at == "u"
