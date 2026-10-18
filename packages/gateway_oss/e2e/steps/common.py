from __future__ import annotations

import json
import os
import re
import struct
import zlib
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


# --- Draft lifecycle ---------------------------------------------------


@when('I create a draft with title "{title}" and body "{body}"')
def step_create_draft(context, title, body):
    context.response = context.client.post(
        "/api/v1/drafts",
        json={"title": title, "body": body},
        headers=context.headers,
    )


@given("the created draft ID is saved")
def step_save_created_draft_id(context):
    data = context.response.json()
    assert "id" in data, f"Expected 'id' in response, got: {list(data.keys())}"
    context.draft_id = str(data["id"])


@when("I fetch the test draft")
def step_fetch_draft(context):
    context.response = context.client.get(
        f"/api/v1/drafts/{context.draft_id}",
        headers=context.headers,
    )


@when('I update the test draft with title "{title}"')
def step_update_draft(context, title):
    context.response = context.client.put(
        f"/api/v1/drafts/{context.draft_id}",
        json={"title": title},
        headers=context.headers,
    )


@when("I delete the test draft")
def step_delete_draft(context):
    context.response = context.client.delete(
        f"/api/v1/drafts/{context.draft_id}",
        headers=context.headers,
    )
    if context.response.status_code in (204, 404):
        context.draft_deleted = True


# --- Rich draft round-trip ---------------------------------------------------

_HOSTED_SIZE_SUFFIX = re.compile(r"_\d+x\d+\.[A-Za-z0-9]+(?:$|[?#])")

# One of every dialect element the round-trip must preserve. `{image_url}` is
# filled in with the Substack-hosted image uploaded earlier in the scenario.
RICH_DIALECT_BODY = """\
::defaults{{align=justify}}

# E2E rich draft

A justified paragraph that follows the default alignment of the whole draft.

:::align{{center}}
A centered paragraph.
:::

:::align{{left}}
A left-aligned paragraph.
:::

![E2E image]({image_url}){{size=large watermark}}

::button[Subscribe now]{{href=subscribe}}

::button[Share this post]{{href=share}}

::button[Leave a comment]{{href=comment}}

---

:::callout
A callout with **bold** text.
:::
"""


def _solid_png(width: int, height: int, rgb: tuple[int, int, int]) -> bytes:
    """Build a solid-colour RGB PNG with the standard library only."""

    def chunk(kind: bytes, data: bytes) -> bytes:
        body = kind + data
        return (
            struct.pack(">I", len(data))
            + body
            + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
        )

    row = b"\x00" + bytes(rgb) * width  # filter byte 0 (None) + pixels
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(row * height))
        + chunk(b"IEND", b"")
    )


@given("a Substack-hosted test image is uploaded")
def step_upload_test_image(context):
    context.response = context.client.post(
        "/api/v1/images",
        files={
            "file": ("e2e-image.png", _solid_png(200, 100, (30, 90, 160)), "image/png")
        },
        headers=context.headers,
    )
    assert context.response.status_code == 201, (
        f"Image upload failed: {context.response.status_code}: {context.response.text}"
    )
    url = context.response.json().get("url", "")
    assert _HOSTED_SIZE_SUFFIX.search(url), (
        f"Uploaded image URL {url!r} has no _<width>x<height> suffix, so "
        "{watermark} cannot size it; this is a finding about Substack's image "
        "URL form, not a test fault."
    )
    context.image_url = url


@when('I create a draft with title "{title}" and the rich dialect body')
def step_create_rich_draft(context, title):
    body = RICH_DIALECT_BODY.format(image_url=context.image_url)
    context.response = context.client.post(
        "/api/v1/drafts",
        json={"title": title, "body": body},
        headers=context.headers,
    )


@when("I update the test draft with the fetched body and updated_at")
def step_update_draft_with_fetched(context):
    fetched = context.response.json()
    assert fetched.get("body"), f"Fetched draft has no body: {fetched}"
    assert fetched.get("updated_at"), f"Fetched draft has no updated_at: {fetched}"
    context.previous_body = fetched["body"]
    context.response = context.client.put(
        f"/api/v1/drafts/{context.draft_id}",
        json={"body": fetched["body"], "expected_updated_at": fetched["updated_at"]},
        headers=context.headers,
    )


@when(
    "I update the test draft again with the previous body and the returned updated_at"
)
def step_update_draft_chained(context):
    # Chained edit: the updated_at comes from the previous PUT's response, not
    # from a fresh GET, so Substack must report the stamp it actually stored.
    updated = context.response.json()
    assert updated.get("updated_at"), f"Update response has no updated_at: {updated}"
    context.response = context.client.put(
        f"/api/v1/drafts/{context.draft_id}",
        json={
            "body": context.previous_body,
            "expected_updated_at": updated["updated_at"],
        },
        headers=context.headers,
    )


_RICH_IMAGE = re.compile(r"^!\[E2E image\]\((\S+)\)\{(.*)\}$", re.MULTILINE)


@then("the fetched body keeps the rich dialect elements")
def step_body_keeps_rich_elements(context):
    body = context.response.json()["body"]
    assert body.startswith("::defaults{align=justify}\n"), (
        f"Expected the justify default as the first line of:\n{body}"
    )
    for needle in (
        ":::align{center}",
        ":::align{left}",
        ":::callout",
        "::button[Subscribe now]{href=subscribe}",
        "::button[Share this post]{href=share}",
        "::button[Leave a comment]{href=comment}",
    ):
        assert needle in body, f"Expected {needle!r} in fetched body:\n{body}"
    assert body.count("::button[") == 3, f"Expected 3 buttons in:\n{body}"
    assert "\n---\n" in body, f"Expected a horizontal rule in:\n{body}"
    image = _RICH_IMAGE.search(body)
    assert image, f"Expected the E2E image line in:\n{body}"
    src, attrs = image.groups()
    assert "size=large" in attrs, f"Expected size=large on the image: {attrs}"
    # The watermark instruction was carried out: the stored picture is a new
    # (watermarked) URL and original= points back at the uploaded image.
    assert "original=" in attrs, f"Expected original= on the image: {attrs}"
    assert context.image_url in attrs, (
        f"Expected original= to name the uploaded image {context.image_url!r}: {attrs}"
    )
    assert src != context.image_url, (
        f"Expected a watermarked image URL, got the original back: {src}"
    )


@then("the fetched body equals the previously fetched body")
def step_body_equals_previous(context):
    body = context.response.json()["body"]
    assert body == context.previous_body, (
        "Round-trip changed the body.\n--- first fetch ---\n"
        f"{context.previous_body}\n--- second fetch ---\n{body}"
    )


@when("I fetch the test draft prepublish")
def step_fetch_draft_prepublish(context):
    context.response = context.client.get(
        f"/api/v1/drafts/{context.draft_id}/prepublish",
        headers=context.headers,
    )


@when("I fetch the test draft AI detection")
def step_fetch_draft_ai_detection(context):
    context.response = context.client.get(
        f"/api/v1/drafts/{context.draft_id}/ai-detection",
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
