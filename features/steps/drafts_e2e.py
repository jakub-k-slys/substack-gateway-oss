from __future__ import annotations

import copy

import httpx
from behave import given

from features.steps.common import load_sample

_CREATED_DRAFT_ID = 189531629


def _draft_url(context, draft_id: int | None = None) -> str:
    pub = context.headers.get("x-publication-url")
    if not pub:
        raise RuntimeError("x-publication-url not set — missing a Given step?")
    base = f"{pub.rstrip('/')}/api/v1/drafts"
    return f"{base}/{draft_id}" if draft_id is not None else base


@given(
    "the Substack drafts list endpoint cycles through initial, after-create, and after-delete responses"
)
def step_drafts_cycling(context):
    """Mock GET /drafts to return different item counts on successive calls.

    Call 1: original 2-item sample     (initial list)
    Call 2: 3 items                    (after create — new draft appended)
    Call 3: original 2 items           (after delete — back to normal)
    """
    base = load_sample("api/v1/drafts/list-response")
    create_resp = load_sample("api/v1/draft/response")

    after_create = copy.deepcopy(base)
    new_draft_item = {
        "id": create_resp["id"],
        "uuid": create_resp["uuid"],
        "publication_id": create_resp.get("publication_id", 2817779),
        "type": create_resp.get("type", "newsletter"),
        "post_date": None,
        "email_sent_at": None,
        "is_published": False,
        "title": "Hello world!",
        "draft_title": "Hello world!",
        "draft_updated_at": create_resp.get("draft_updated_at"),
        "audience": create_resp.get("audience", "only_paid"),
        "slug": None,
        "should_send_email": False,
        "write_comment_permissions": "everyone",
        "default_comment_sort": None,
        "section_id": None,
        "cover_image": None,
        "podcast_art_url": None,
        "section_slug": None,
        "section_name": None,
        "is_section_pinned": False,
        "reactions": {"❤": 0},
        "reaction": None,
        "top_exclusions": [],
        "pins": [],
        "videoUpload": None,
        "podcastUpload": None,
        "podcastPreviewUpload": None,
        "voiceoverUpload": None,
        "publishedBylines": [],
        "reaction_count": 0,
        "comment_count": 0,
        "child_comment_count": 0,
    }
    after_create.append(new_draft_item)

    responses = iter(
        [
            httpx.Response(200, json=base),
            httpx.Response(200, json=after_create),
            httpx.Response(200, json=base),
        ]
    )

    context.respx_mock.get(_draft_url(context)).mock(
        side_effect=lambda _request: next(responses)
    )


@given(
    "the Substack get-draft endpoint returns the created draft for draft {draft_id:d}"
)
def step_get_created_draft(context, draft_id):
    """Return a draft whose fields match the create request."""
    body_json = (
        '{"type":"doc","content":'
        '[{"type":"paragraph","content":'
        '[{"type":"text","text":"Hello world!"}]}]}'
    )
    context.respx_mock.get(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(
            200,
            json={
                "id": draft_id,
                "uuid": "f0deca7a-b4c0-4389-9b0b-d4239790d914",
                "draft_title": "Hello world!",
                "draft_subtitle": "A test draft",
                "draft_body": body_json,
                "audience": "only_paid",
                "type": "newsletter",
                "is_published": False,
                "draft_created_at": "2026-03-01T08:26:49.556Z",
                "draft_updated_at": "2026-03-01T08:26:49.556Z",
            },
        )
    )


@given(
    "the Substack update-draft endpoint returns the updated draft for draft {draft_id:d}"
)
def step_update_created_draft(context, draft_id):
    """Return a draft with the updated title."""
    body_json = (
        '{"type":"doc","content":'
        '[{"type":"paragraph","content":'
        '[{"type":"text","text":"Hello world!"}]}]}'
    )
    context.respx_mock.put(_draft_url(context, draft_id)).mock(
        return_value=httpx.Response(
            200,
            json={
                "id": draft_id,
                "uuid": "f0deca7a-b4c0-4389-9b0b-d4239790d914",
                "draft_title": "Updated title",
                "draft_subtitle": "A test draft",
                "draft_body": body_json,
                "audience": "only_paid",
                "type": "newsletter",
                "is_published": False,
                "draft_created_at": "2026-03-01T08:26:49.556Z",
                "draft_updated_at": "2026-03-01T09:00:00.000Z",
            },
        )
    )
