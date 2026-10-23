from __future__ import annotations

import importlib
import os

import respx
from starlette.testclient import TestClient

os.environ["SUBSTACK_GATEWAY_DISABLE_ENTRYPOINT_EXTENSIONS"] = "1"

from gateway_oss import create_app

app = create_app()

_BEHAVE_SUBSTACK_MAX_CONNECTIONS = 100
_BEHAVE_SUBSTACK_MAX_KEEPALIVE_CONNECTIONS = 100


def before_all(context):
    from gateway_oss.config import settings

    context._original_substack_max_connections = settings.substack_max_connections
    context._original_substack_max_keepalive_connections = (
        settings.substack_max_keepalive_connections
    )

    settings.substack_max_connections = _BEHAVE_SUBSTACK_MAX_CONNECTIONS
    settings.substack_max_keepalive_connections = (
        _BEHAVE_SUBSTACK_MAX_KEEPALIVE_CONNECTIONS
    )


def before_scenario(context, scenario):
    context.client = TestClient(app, raise_server_exceptions=False)
    context.headers: dict[str, str] = {}
    context.response = None
    context.mcp_result = None
    context.mcp_error = None
    context.respx_mock = respx.mock(assert_all_mocked=True)
    context.respx_mock.start()


def after_scenario(context, scenario):
    context.respx_mock.stop()

    # Restore UnitOfWork and base_url if patched by login-flow OAuth steps
    if hasattr(context, "_original_uow"):
        from gateway_pro.config import pro_settings

        login_mod = importlib.import_module("gateway_pro.oauth.login")

        login_mod.UnitOfWork = context._original_uow
        pro_settings.base_url = context._original_base_url

    # Restore UnitOfWork and jwt_secret if patched by provider token-flow steps
    if hasattr(context, "_orig_provider_uow"):
        from gateway_pro.config import pro_settings

        provider_mod = importlib.import_module("gateway_pro.oauth.provider")

        provider_mod.UnitOfWork = context._orig_provider_uow
        pro_settings.jwt_secret = context._orig_jwt_secret


def after_all(context):
    from gateway_oss.config import settings

    settings.substack_max_connections = context._original_substack_max_connections
    settings.substack_max_keepalive_connections = (
        context._original_substack_max_keepalive_connections
    )
