from __future__ import annotations

import base64
import json
import pathlib

from behave import given, then, when

# Shared constants used across step files
SUBSTACK_BASE = "https://substack.com"
SAMPLES_DIR = pathlib.Path(__file__).parent.parent.parent / "samples"

_USER_SETTING_PATH = "/api/v1/user-setting"
_PUBLIC_PROFILE_PATH = "/api/v1/user/{slug}/public_profile"


def load_sample(path: str):
    return json.loads((SAMPLES_DIR / path).read_text())


def pub_url(context) -> str:
    return context.headers.get("x-publication-url", "").rstrip("/")


def user_setting_url() -> str:
    return f"{SUBSTACK_BASE}{_USER_SETTING_PATH}"


def public_profile_url(slug: str) -> str:
    return f"{SUBSTACK_BASE}{_PUBLIC_PROFILE_PATH.format(slug=slug)}"


@given('a valid bearer token "{token}" and publication URL "{pub_url_}"')
def step_valid_auth(context, token, pub_url_):
    credentials = {"substack_sid": token, "connect_sid": token, "gateway_key": "test"}
    encoded = base64.b64encode(json.dumps(credentials).encode()).decode()
    context.headers = {
        "Authorization": f"Bearer {encoded}",
        "x-publication-url": pub_url_,
    }


@given('a malformed authorization header and publication URL "{pub_url_}"')
def step_malformed_auth(context, pub_url_):
    context.headers = {
        "Authorization": "not-a-bearer-token",
        "x-publication-url": pub_url_,
    }


@given('a bearer token with extra whitespace and publication URL "{pub_url_}"')
def step_whitespace_token(context, pub_url_):
    credentials = {
        "substack_sid": "test-token",
        "connect_sid": "test-token",
        "gateway_key": "test",
    }
    encoded = base64.b64encode(json.dumps(credentials).encode()).decode()
    context.headers = {
        "Authorization": f"Bearer   {encoded}   ",
        "x-publication-url": pub_url_,
    }


@when("I send GET {path}")
def step_get(context, path):
    context.response = context.client.get(path, headers=context.headers)


@when("I send POST {path} with JSON body {body}")
def step_post_json(context, path, body):
    context.response = context.client.post(
        path, json=json.loads(body), headers=context.headers
    )


@then("the response status code is {status:d}")
def step_status_code(context, status):
    actual = context.response.status_code
    assert actual == status, (
        f"Expected status {status}, got {actual}. Body: {context.response.text}"
    )


@then('the response field "{field}" is true')
def step_field_true(context, field):
    body = context.response.json()
    assert body[field] is True, (
        f'Expected field "{field}" to be true, got {body[field]}'
    )


@then('the response field "{field}" is false')
def step_field_false(context, field):
    body = context.response.json()
    assert body[field] is False, (
        f'Expected field "{field}" to be false, got {body[field]}'
    )


@then('the response field "{field}" is "{value}"')
def step_field_string(context, field, value):
    body = context.response.json()
    assert body[field] == value, (
        f'Expected field "{field}" to be "{value}", got "{body[field]}"'
    )


@then('the response field "{field}" is not null')
def step_field_not_null(context, field):
    body = context.response.json()
    assert body[field] is not None, f'Expected field "{field}" to be non-null, got null'


@then('the response field "{field}" is absent')
def step_field_absent(context, field):
    body = context.response.json()
    assert field not in body, (
        f'Expected field "{field}" to be absent, got {body[field]}'
    )


@then('the response list "{field}" has {count:d} item')
def step_list_count_singular(context, field, count):
    body = context.response.json()
    actual = len(body[field])
    assert actual == count, f'Expected "{field}" to have {count} item(s), got {actual}'


@then('the response list "{field}" has {count:d} items')
def step_list_count_plural(context, field, count):
    step_list_count_singular(context, field, count)


@then('the response nested field "{parent}.{child}" is "{value}"')
def step_nested_field_string(context, parent, child, value):
    body = context.response.json()
    actual = body[parent][child]
    assert actual == value, (
        f'Expected "{parent}.{child}" to be "{value}", got "{actual}"'
    )


@then('the first item field "{field}" is "{value}"')
def step_first_item_field(context, field, value):
    body = context.response.json()
    items = body.get("items", [])
    assert items, "Response list 'items' is empty"
    actual = items[0][field]
    assert actual == value, (
        f'Expected first item "{field}" to be "{value}", got "{actual}"'
    )
