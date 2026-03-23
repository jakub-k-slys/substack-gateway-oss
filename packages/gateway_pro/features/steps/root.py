from __future__ import annotations

from behave import then
from gateway_pro import __version__


@then('the response field "{field}" matches the PRO package version')
def step_field_matches_package_version(context, field):
    body = context.response.json()
    assert body[field] == __version__, (
        f'Expected field "{field}" to be "{__version__}", got "{body[field]}"'
    )
