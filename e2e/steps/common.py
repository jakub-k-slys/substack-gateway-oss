from __future__ import annotations

import os
from urllib.parse import urlparse

from behave import given, then, when


@given("valid credentials")
def step_valid_credentials(context):
    token = os.environ["SUBSTACK_TOKEN"]
    pub_url = os.environ["SUBSTACK_PUBLICATION_URL"]
    context.headers["Authorization"] = f"Bearer {token}"
    context.headers["x-publication-url"] = pub_url


@given("a valid publication URL")
def step_valid_publication_url(context):
    pub_url = os.environ.get("SUBSTACK_PUBLICATION_URL", "")
    parsed = urlparse(pub_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        context.scenario.skip(
            "SUBSTACK_PUBLICATION_URL not configured or not a valid HTTP/HTTPS URL"
        )


@when("I GET {path}")
def step_get(context, path):
    context.response = context.client.get(path, headers=context.headers)


@then("the response status is {status:d}")
def step_status(context, status):
    assert context.response.status_code == status, (
        f"Expected {status}, got {context.response.status_code}: {context.response.text}"
    )


@then('the response has field "{field}"')
def step_has_field(context, field):
    data = context.response.json()
    assert field in data, (
        f"Expected field '{field}' in response, got keys: {list(data.keys())}"
    )


@then("the response is a list")
def step_is_list(context):
    data = context.response.json()
    assert isinstance(data, list), f"Expected a list, got: {type(data).__name__}"


@then('the response field "{field}" is a list')
def step_field_is_list(context, field):
    data = context.response.json()
    assert field in data, f"Expected field '{field}' in response"
    assert isinstance(data[field], list), f"Expected '{field}' to be a list"


@given("a test profile slug")
def step_profile_slug(context):
    slug = os.environ.get("E2E_PROFILE_SLUG", "")
    if not slug:
        context.scenario.skip("E2E_PROFILE_SLUG not configured")
    context.profile_slug = slug


@when("I fetch the test profile")
def step_get_profile(context):
    context.response = context.client.get(
        f"/api/v1/profiles/{context.profile_slug}", headers=context.headers
    )


@when("I fetch the test profile posts")
def step_get_profile_posts(context):
    context.response = context.client.get(
        f"/api/v1/profiles/{context.profile_slug}/posts", headers=context.headers
    )


@when("I fetch the test profile notes")
def step_get_profile_notes(context):
    context.response = context.client.get(
        f"/api/v1/profiles/{context.profile_slug}/notes", headers=context.headers
    )


@given("a test note ID")
def step_note_id(context):
    note_id = os.environ.get("E2E_NOTE_ID", "")
    if not note_id:
        context.scenario.skip("E2E_NOTE_ID not configured")
    context.note_id = note_id


@when("I fetch the test note")
def step_get_note(context):
    context.response = context.client.get(
        f"/api/v1/notes/{context.note_id}", headers=context.headers
    )


@when('I create a note with content "{content}"')
def step_create_note(context, content):
    context.response = context.client.post(
        "/api/v1/notes",
        json={"content": content},
        headers=context.headers,
    )


@given("the created note ID is saved")
def step_save_created_note_id(context):
    data = context.response.json()
    assert "id" in data, f"Expected 'id' in response, got: {list(data.keys())}"
    context.note_id = str(data["id"])


@when("I delete the test note")
def step_delete_note(context):
    context.response = context.client.delete(
        f"/api/v1/notes/{context.note_id}", headers=context.headers
    )


@given("a test post ID")
def step_post_id(context):
    post_id = os.environ.get("E2E_POST_ID", "")
    if not post_id:
        context.scenario.skip("E2E_POST_ID not configured")
    context.post_id = post_id


@when("I fetch the test post")
def step_get_post(context):
    context.response = context.client.get(
        f"/api/v1/posts/{context.post_id}", headers=context.headers
    )


@when("I fetch the test post comments")
def step_get_post_comments(context):
    context.response = context.client.get(
        f"/api/v1/posts/{context.post_id}/comments", headers=context.headers
    )
