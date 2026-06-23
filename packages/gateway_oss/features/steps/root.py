from __future__ import annotations

from behave import then

from gateway_oss import __version__


def _module(context, name):
    body = context.response.json()
    modules = body["modules"]
    for module in modules:
        if module["name"] == name:
            return module
    raise AssertionError(f'No module named "{name}" in {modules!r}')


@then('the response contains a module named "{name}"')
def step_response_contains_module(context, name):
    _module(context, name)


@then('the "{name}" module version matches the OSS package version')
def step_module_version_matches(context, name):
    module = _module(context, name)
    assert module["version"] == __version__, (
        f'Expected "{name}" module version "{__version__}", got "{module["version"]}"'
    )


@then('the "{name}" module features contain "{feature}"')
def step_module_features_contain(context, name, feature):
    module = _module(context, name)
    assert feature in module["features"], (
        f'Expected "{name}" module features to contain "{feature}"'
    )
