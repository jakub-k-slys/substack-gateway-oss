from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from gateway_drafts.service import DraftsService


class _Resp:
    def __init__(self, payload: object) -> None:
        self._p = payload

    def json(self) -> object:
        return self._p


def _service(pub: AsyncMock) -> DraftsService:
    return DraftsService(pub, AsyncMock())


@pytest.mark.anyio
async def test_ai_detection_parses_pangram_fields() -> None:
    pub = AsyncMock()
    pub.get.return_value = _Resp(
        {
            "type": "success",
            "header": "Fully AI-assisted text",
            "details": "Analysis by Pangram ...",
            "fraction_ai": 1,
            "fraction_ai_assisted": 0,
            "fraction_human": 0,
            "can_disable": True,
            "can_modify_disclosure": True,
            "disclosure": {"pub": {"x": 1}},
        }
    )
    result = await _service(pub).ai_detection(208563951)
    pub.get.assert_awaited_once_with("drafts/208563951/pangram_detection")
    assert result.fraction_ai == 1
    assert result.header == "Fully AI-assisted text"
    assert result.can_disable is True


@pytest.mark.anyio
async def test_prepublish_draft_parses_errors_and_suggestions() -> None:
    pub = AsyncMock()
    pub.get.return_value = _Resp({"errors": [], "suggestions": ["add a subtitle"]})
    result = await _service(pub).prepublish_draft(208563951)
    pub.get.assert_awaited_once_with("drafts/208563951/prepublish")
    assert result.errors == []
    assert result.suggestions == ["add a subtitle"]


@pytest.mark.anyio
async def test_schedule_draft_posts_scheduled_release_payload() -> None:
    pub = AsyncMock()
    when = datetime(2026, 9, 16, 18, 24, tzinfo=UTC)
    release = await _service(pub).schedule_draft(208563951, when)
    pub.post.assert_awaited_once_with(
        "drafts/208563951/scheduled_release",
        json={
            "trigger_at": "2026-09-16T18:24:00.000Z",
            "post_audience": "only_paid",
            "email_audience": "only_paid",
        },
    )
    assert release.trigger_at == "2026-09-16T18:24:00.000Z"


@pytest.mark.anyio
async def test_schedule_draft_accepts_iso_string_and_custom_audience() -> None:
    pub = AsyncMock()
    await _service(pub).schedule_draft(
        1, "2026-09-16T18:24:00Z", post_audience="everyone", email_audience="everyone"
    )
    pub.post.assert_awaited_once_with(
        "drafts/1/scheduled_release",
        json={
            "trigger_at": "2026-09-16T18:24:00.000Z",
            "post_audience": "everyone",
            "email_audience": "everyone",
        },
    )


@pytest.mark.anyio
async def test_unschedule_draft_deletes_scheduled_release() -> None:
    pub = AsyncMock()
    await _service(pub).unschedule_draft(208563951)
    pub.delete.assert_awaited_once_with("drafts/208563951/scheduled_release")
