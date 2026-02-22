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


@then('the response list "{field}" has {count:d} item')
def step_list_count_singular(context, field, count):
    body = context.response.json()
    actual = len(body[field])
    assert actual == count, f'Expected "{field}" to have {count} item(s), got {actual}'


@then('the response list "{field}" has {count:d} items')
def step_list_count_plural(context, field, count):
    step_list_count_singular(context, field, count)


@then('the first item field "{field}" is "{value}"')
def step_first_item_field(context, field, value):
    body = context.response.json()
    items = body.get("items", [])
    assert items, "Response list 'items' is empty"
    actual = items[0][field]
    assert actual == value, (
        f'Expected first item "{field}" to be "{value}", got "{actual}"'
    )
