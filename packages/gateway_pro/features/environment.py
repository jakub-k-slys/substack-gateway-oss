from __future__ import annotations

import asyncio
import os

import respx
from starlette.testclient import TestClient

os.environ.pop("SUBSTACK_GATEWAY_DISABLE_ENTRYPOINT_EXTENSIONS", None)

from gateway_oss.config import settings
from gateway_oss.main import app
from gateway_pro.config import pro_settings
from gateway_pro.services.following_feed import FollowingFeedService

_BEHAVE_SUBSTACK_REQUESTS_PER_SECOND = 100.0
_BEHAVE_SUBSTACK_MAX_CONNECTIONS = 100
_BEHAVE_SUBSTACK_MAX_KEEPALIVE_CONNECTIONS = 100
_BEHAVE_SUBSTACK_RETRY_ATTEMPTS = 1
_BEHAVE_SUBSTACK_RETRY_WAIT_SEC = 1.0


def _clear_following_feed_cache() -> None:
    asyncio.run(FollowingFeedService._get_followed_profile_entries.cache.clear())


def before_all(context):
    context._original_substack_requests_per_second = (
        settings.substack_requests_per_second
    )
    context._original_substack_max_connections = settings.substack_max_connections
    context._original_substack_max_keepalive_connections = (
        settings.substack_max_keepalive_connections
    )
    context._original_substack_retry_attempts = settings.substack_retry_attempts
    context._original_substack_retry_min_wait_sec = settings.substack_retry_min_wait_sec
    context._original_substack_retry_max_wait_sec = settings.substack_retry_max_wait_sec

    settings.substack_requests_per_second = _BEHAVE_SUBSTACK_REQUESTS_PER_SECOND
    settings.substack_max_connections = _BEHAVE_SUBSTACK_MAX_CONNECTIONS
    settings.substack_max_keepalive_connections = (
        _BEHAVE_SUBSTACK_MAX_KEEPALIVE_CONNECTIONS
    )
    settings.substack_retry_attempts = _BEHAVE_SUBSTACK_RETRY_ATTEMPTS
    settings.substack_retry_min_wait_sec = _BEHAVE_SUBSTACK_RETRY_WAIT_SEC
    settings.substack_retry_max_wait_sec = _BEHAVE_SUBSTACK_RETRY_WAIT_SEC


def before_scenario(context, scenario):
    _clear_following_feed_cache()
    context.client = TestClient(app, raise_server_exceptions=False)
    context.headers: dict[str, str] = {}
    context.response = None
    context.mcp_result = None
    context.mcp_error = None
    context.respx_mock = respx.mock(assert_all_mocked=True)
    context.respx_mock.start()


def after_scenario(context, scenario):
    context.respx_mock.stop()
    _clear_following_feed_cache()

    # Restore UnitOfWork and base_url if patched by login-flow OAuth steps
    if hasattr(context, "_original_uow"):
        import gateway_pro.oauth.login as login_mod

        login_mod.UnitOfWork = context._original_uow
        pro_settings.base_url = context._original_base_url

    # Restore UnitOfWork and jwt_secret if patched by provider token-flow steps
    if hasattr(context, "_orig_provider_uow"):
        import gateway_pro.oauth.provider as provider_mod

        provider_mod.UnitOfWork = context._orig_provider_uow
        pro_settings.jwt_secret = context._orig_jwt_secret


def after_all(context):
    settings.substack_requests_per_second = (
        context._original_substack_requests_per_second
    )
    settings.substack_max_connections = context._original_substack_max_connections
    settings.substack_max_keepalive_connections = (
        context._original_substack_max_keepalive_connections
    )
    settings.substack_retry_attempts = context._original_substack_retry_attempts
    settings.substack_retry_min_wait_sec = context._original_substack_retry_min_wait_sec
    settings.substack_retry_max_wait_sec = context._original_substack_retry_max_wait_sec


__all__ = ["before_all", "before_scenario", "after_scenario", "after_all"]
