from gateway_drafts.models.substack import SubstackDraft
from gateway_drafts.schemas import DraftResponse


def test_draft_response_carries_publication_state() -> None:
    draft = SubstackDraft.model_validate(
        {
            "draft_title": "t",
            "draft_updated_at": "u",
            "audience": "everyone",
            "is_published": False,
            "post_date": None,
            "postSchedules": [
                {
                    "id": 13823941,
                    "trigger_at": "2027-01-15T15:00:00.000Z",
                    "post_audience": "everyone",
                    "email_audience": "everyone",
                }
            ],
        }
    )
    resp = DraftResponse.from_substack(draft)
    assert resp.audience == "everyone"
    assert resp.is_published is False
    assert resp.post_date is None
    assert [s.trigger_at for s in resp.scheduled_releases] == [
        "2027-01-15T15:00:00.000Z"
    ]
    assert resp.scheduled_releases[0].email_audience == "everyone"


def test_draft_response_without_schedules_is_empty_list() -> None:
    resp = DraftResponse.from_substack(SubstackDraft(draft_updated_at="u"))
    assert resp.scheduled_releases == []
    assert resp.audience is None
