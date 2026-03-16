from __future__ import annotations

from gateway.models.schemas import DraftResponse, UpdateDraftRequest
from gateway.models.substack import SubstackUpdateDraftPayload
from gateway_pro.converters.markdown import (
    draft_body_to_markdown,
    markdown_to_draft_body,
)
from gateway_pro.models.substack import SubstackDraft


def test_shared_update_draft_request_uses_pro_payload_and_converter() -> None:
    payload = UpdateDraftRequest(body="**bold**").to_substack_payload()

    assert isinstance(payload, SubstackUpdateDraftPayload)
    assert payload.draft_body == markdown_to_draft_body("**bold**")


def test_shared_draft_response_round_trips_through_pro_converter() -> None:
    draft = SubstackDraft(
        draft_title="Title",
        draft_subtitle="Subtitle",
        draft_body=markdown_to_draft_body("> quoted"),
    )

    response = DraftResponse.from_substack(draft)

    assert response.title == "Title"
    assert response.subtitle == "Subtitle"
    assert response.body == draft_body_to_markdown(draft.draft_body or "")
