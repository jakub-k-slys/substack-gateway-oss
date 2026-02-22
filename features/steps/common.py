from __future__ import annotations

from behave import given, then, when


@given('a valid bearer token "{token}" and publication URL "{pub_url}"')
def step_valid_auth(context, token, pub_url):
    context.headers = {
        "Authorization": f"Bearer {token}",
        "x-publication-url": pub_url,
    }


@given('a malformed authorization header and publication URL "{pub_url}"')
def step_malformed_auth(context, pub_url):
    context.headers = {
        "Authorization": "not-a-bearer-token",
        "x-publication-url": pub_url,
    }


@when("I send GET {path}")
def step_get(context, path):
    context.response = context.client.get(path, headers=context.headers)


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
