from __future__ import annotations

from behave import then

from gateway_oss import __app_version__


@then('the response field "{field}" matches the OSS package version')
def step_field_matches_package_version(context, field):
    body = context.response.json()
    assert body[field] == __app_version__, (
        f'Expected field "{field}" to be "{__app_version__}", got "{body[field]}"'
    )
