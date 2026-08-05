from __future__ import annotations

import json
import os
from urllib.parse import urlparse

from behave import given, then, when


def _required_env(context, name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        context.scenario.skip(f"{name} not configured")
    return value


@given("valid credentials")
def step_valid_credentials(context):
    token = (
        os.environ.get("SUBSTACK_GATEWAY_TOKEN", "").strip()
        or os.environ.get("SUBSTACK_TOKEN", "").strip()
    )
    if not token:
        context.scenario.skip("SUBSTACK_GATEWAY_TOKEN or SUBSTACK_TOKEN not configured")
    context.headers["x-gateway-token"] = token


@given("a valid publication URL")
def step_valid_publication_url(context):
    pub_url = _required_env(context, "SUBSTACK_PUBLICATION_URL")
    parsed = urlparse(pub_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        context.scenario.skip(
            "SUBSTACK_PUBLICATION_URL not configured or not a valid HTTP/HTTPS URL"
        )


@given("a test profile slug")
def step_profile_slug(context):
    context.profile_slug = _required_env(context, "E2E_PROFILE_SLUG")


@given("a test note ID")
def step_note_id(context):
    context.note_id = _required_env(context, "E2E_NOTE_ID")


@given("a test post ID")
def step_post_id(context):
    context.post_id = _required_env(context, "E2E_POST_ID")


@when("I GET {path}")
def step_get(context, path):
    context.response = context.client.get(path, headers=context.headers)


@when("I fetch the test profile")
def step_get_profile(context):
    context.response = context.client.get(
        f"/api/v1/profiles/{context.profile_slug}",
        headers=context.headers,
    )


@when("I fetch the test profile posts")
def step_get_profile_posts(context):
    context.response = context.client.get(
        f"/api/v1/profiles/{context.profile_slug}/posts",
        headers=context.headers,
    )


@when("I fetch the test profile notes")
def step_get_profile_notes(context):
    context.response = context.client.get(
        f"/api/v1/profiles/{context.profile_slug}/notes",
        headers=context.headers,
    )


@when("I fetch the test note")
def step_get_note(context):
    context.response = context.client.get(
        f"/api/v1/notes/{context.note_id}",
        headers=context.headers,
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
        f"/api/v1/notes/{context.note_id}",
        headers=context.headers,
    )


@when("I fetch the test post")
def step_get_post(context):
    context.response = context.client.get(
        f"/api/v1/posts/{context.post_id}",
        headers=context.headers,
    )


@when("I fetch the test post comments")
def step_get_post_comments(context):
    context.response = context.client.get(
        f"/api/v1/posts/{context.post_id}/comments",
        headers=context.headers,
    )


# --- Post comment lifecycle -------------------------------------------------


@when('I create a post comment with body "{body}"')
def step_create_post_comment(context, body):
    context.response = context.client.post(
        f"/api/v1/posts/{context.post_id}/comments",
        json={"body": body},
        headers=context.headers,
    )


@given("the created post comment ID is saved as the top")
def step_save_top_post_comment(context):
    context.top_post_comment_id = str(context.response.json()["id"])


@given("the created post comment ID is saved as the reply")
def step_save_reply_post_comment(context):
    context.reply_post_comment_id = str(context.response.json()["id"])


@when('I reply to the top post comment with body "{body}"')
def step_reply_to_top(context, body):
    context.response = context.client.post(
        f"/api/v1/comments/{context.top_post_comment_id}/comments",
        json={"body": body},
        headers=context.headers,
    )


@when('I reply to post comment "{comment_id}" with body "{body}"')
def step_reply_to_explicit(context, comment_id, body):
    context.response = context.client.post(
        f"/api/v1/comments/{comment_id}/comments",
        json={"body": body},
        headers=context.headers,
    )


@when("I list replies of the top post comment")
def step_list_replies_of_top(context):
    context.response = context.client.get(
        f"/api/v1/comments/{context.top_post_comment_id}/comments",
        headers=context.headers,
    )


@then("the items contain the reply post comment")
def step_items_contain_reply(context):
    items = context.response.json()["items"]
    target = int(context.reply_post_comment_id)
    assert any(it["id"] == target for it in items), (
        f"reply id={target} not in listing: {[it['id'] for it in items]}"
    )


@when("I fetch the top post comment")
def step_fetch_top(context):
    context.response = context.client.get(
        f"/api/v1/comments/{context.top_post_comment_id}", headers=context.headers
    )


@when("I like the top post comment")
def step_like_top(context):
    context.response = context.client.post(
        f"/api/v1/comments/{context.top_post_comment_id}/reaction",
        headers=context.headers,
    )


@when("I unlike the top post comment")
def step_unlike_top(context):
    context.response = context.client.delete(
        f"/api/v1/comments/{context.top_post_comment_id}/reaction",
        headers=context.headers,
    )


@when("I delete the reply post comment")
def step_delete_reply_post_comment(context):
    context.response = context.client.delete(
        f"/api/v1/comments/{context.reply_post_comment_id}",
        headers=context.headers,
    )


@when("I delete the top post comment")
def step_delete_top_post_comment(context):
    context.response = context.client.delete(
        f"/api/v1/comments/{context.top_post_comment_id}",
        headers=context.headers,
    )


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


@then('the response field "{field}" is "{value}"')
def step_field_equals(context, field, value):
    data = context.response.json()
    actual = data.get(field)
    assert actual == value, f"Expected '{field}' to be '{value}', got '{actual}'"


@then('the response nested field "{field}" is a list')
def step_nested_field_is_list(context, field):
    data = context.response.json()
    value = data
    for part in field.split("."):
        value = value[part]
    assert isinstance(value, list), f"Expected '{field}' to be a list"


@then('the response nested field "{field}" is not null')
def step_nested_field_not_null(context, field):
    data = context.response.json()
    value = data
    for part in field.split("."):
        value = value[part]
    assert value is not None, f"Expected '{field}' to be non-null"


@then("the response body is valid JSON")
def step_valid_json(context):
    json.loads(context.response.text)
