from __future__ import annotations

import respx
from starlette.testclient import TestClient

from main import application


def before_scenario(context, scenario):
    context.client = TestClient(application, raise_server_exceptions=False)
    context.headers: dict[str, str] = {}
    context.response = None
    context.respx_mock = respx.mock(assert_all_mocked=True)
    context.respx_mock.start()


def after_scenario(context, scenario):
    context.respx_mock.stop()
