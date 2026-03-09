from __future__ import annotations

import respx
from starlette.testclient import TestClient

from main import app


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
        import gateway.oauth.login as login_mod
        from gateway.config import settings

        login_mod.UnitOfWork = context._original_uow
        settings.base_url = context._original_base_url

    # Restore UnitOfWork and jwt_secret if patched by provider token-flow steps
    if hasattr(context, "_orig_provider_uow"):
        import gateway.oauth.provider as provider_mod
        from gateway.config import settings

        provider_mod.UnitOfWork = context._orig_provider_uow
        settings.jwt_secret = context._orig_jwt_secret
