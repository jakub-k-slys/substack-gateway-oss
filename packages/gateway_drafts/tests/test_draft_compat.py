from __future__ import annotations

from gateway_drafts.converters.markdown import (
    draft_body_to_markdown,
    markdown_to_draft_body,
)
from gateway_drafts.models.substack import SubstackDraft
from gateway_drafts.schemas import DraftResponse, UpdateDraftRequest


def test_update_request_reports_only_provided_fields() -> None:
    assert UpdateDraftRequest(body="**bold**").provided_updates() == {
        "body": "**bold**"
    }
    assert UpdateDraftRequest(title="T", body="x").provided_updates() == {
        "title": "T",
        "body": "x",
    }


def test_shared_draft_response_round_trips_through_markdown_converter() -> None:
    draft = SubstackDraft(
        draft_title="Title",
        draft_subtitle="Subtitle",
        draft_body=markdown_to_draft_body("> quoted"),
    )

    response = DraftResponse.from_substack(draft)

    assert response.title == "Title"
    assert response.subtitle == "Subtitle"
    assert response.body == draft_body_to_markdown(draft.draft_body or "")
