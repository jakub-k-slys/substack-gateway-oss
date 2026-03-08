from __future__ import annotations

import copy

import httpx
from behave import given

from features.steps.common import load_sample, pub_url


def _notes_url(context) -> str:
    return f"{pub_url(context)}/api/v1/notes"


@given(
    "the Substack notes endpoint cycles through initial, after-create, and after-delete responses"
)
def step_notes_cycling(context):
    """Mock GET /notes to return different item counts on successive calls.

    Call 1: original 20-item sample  (initial list)
    Call 2: 21 items                 (after create — new note prepended)
    Call 3: original 20 items        (after delete — back to normal)
    """
    base = load_sample("api/v1/notes")
    created = load_sample("api/v1/reader/comment/131719084")

    after_create = copy.deepcopy(base)
    new_note_item = {
        "entity_key": "c-131719084",
        "type": "comment",
        "context": created["item"]["context"],
        "publication": None,
        "post": None,
        "comment": created["item"]["comment"],
        "parentComments": [],
        "canReply": True,
        "isMuted": False,
        "trackingParameters": created["item"]["trackingParameters"],
    }
    after_create["items"].insert(0, new_note_item)

    responses = iter(
        [
            httpx.Response(200, json=base),
            httpx.Response(200, json=after_create),
            httpx.Response(200, json=base),
        ]
    )

    context.respx_mock.get(_notes_url(context)).mock(
        side_effect=lambda _request: next(responses)
    )
