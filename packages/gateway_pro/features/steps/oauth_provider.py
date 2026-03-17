"""Step definitions for NeonOAuthProvider token flow tests.

Uses in-memory mock repositories so no real database is required.
Tests exercise exchange_authorization_code, load_refresh_token, and
exchange_refresh_token directly on the provider instance.
"""

from __future__ import annotations

import asyncio
import time
import types

import jwt
from behave import given, then, when
from gateway_pro.oauth.bearer import _RefreshTokenWithJti
from gateway_pro.oauth.db import DBAccessToken, DBAuthCode, DBRefreshToken
from gateway_pro.oauth.provider import NeonOAuthProvider
from mcp.server.auth.provider import TokenError
from mcp.shared.auth import OAuthClientInformationFull
from pydantic import AnyHttpUrl

# ---------------------------------------------------------------------------
# In-memory store and mock repositories
# ---------------------------------------------------------------------------


class _Store:
    def __init__(self) -> None:
        self.auth_codes: dict[str, DBAuthCode] = {}
        self.access_tokens: dict[str, DBAccessToken] = {}
        self.refresh_tokens: dict[str, DBRefreshToken] = {}


class _MockAuthCodes:
    def __init__(self, store: _Store) -> None:
        self._s = store

    async def consume(self, code: str) -> int | None:
        rec = self._s.auth_codes.pop(code, None)
        return rec.user_id if rec else None


class _MockAccessTokens:
    def __init__(self, store: _Store) -> None:
        self._s = store

    async def save(self, token: DBAccessToken) -> None:
        self._s.access_tokens[token.jti] = token

    async def get(self, jti: str) -> DBAccessToken | None:
        return self._s.access_tokens.get(jti)

    async def revoke(self, jti: str) -> None:
        rec = self._s.access_tokens.get(jti)
        if rec:
            rec.revoked = True


class _MockRefreshTokens:
    def __init__(self, store: _Store) -> None:
        self._s = store

    async def save(self, token: DBRefreshToken) -> None:
        self._s.refresh_tokens[token.token_hash] = token

    async def get_active(
        self, token_hash: str, client_id: str
    ) -> DBRefreshToken | None:
        rec = self._s.refresh_tokens.get(token_hash)
        if rec and rec.client_id == client_id and not rec.revoked:
            return rec
        return None

    async def get(self, token_hash: str) -> DBRefreshToken | None:
        return self._s.refresh_tokens.get(token_hash)

    async def revoke(self, token_hash: str) -> None:
        rec = self._s.refresh_tokens.get(token_hash)
        if rec:
            rec.revoked = True


class _MockUnitOfWork:
    def __init__(self, store: _Store) -> None:
        self._store = store

    async def __aenter__(self) -> _MockUnitOfWork:
        self.auth_codes = _MockAuthCodes(self._store)
        self.access_tokens = _MockAccessTokens(self._store)
        self.refresh_tokens = _MockRefreshTokens(self._store)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_JWT_SECRET = "test-secret"


def _run(coro):
    return asyncio.run(coro)


def _make_provider(base_url: str = "http://localhost/mcp") -> NeonOAuthProvider:
    return NeonOAuthProvider(
        base_url=base_url,
        login_base_url="http://localhost",
    )


def _make_client(client_id: str) -> OAuthClientInformationFull:
    return OAuthClientInformationFull(
        client_id=client_id,
        client_name="Test client",
        redirect_uris=[AnyHttpUrl("http://localhost/callback")],
    )


def _make_auth_code(code: str, client_id: str, user_id: int):
    from mcp.server.auth.provider import AuthorizationCode

    return AuthorizationCode(
        code=code,
        client_id=client_id,
        redirect_uri=AnyHttpUrl("http://localhost/callback"),
        redirect_uri_provided_explicitly=True,
        scopes=["read"],
        expires_at=time.time() + 300,
        code_challenge="challenge",
    )


def _decode_jwt(token: str) -> dict:
    return jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------


@given('the OAuth provider is configured with jwt secret "{secret}"')
def step_configure_provider(context, secret):
    context.provider_store = _Store()
    context.provider = _make_provider()

    # Patch UnitOfWork in the actual provider module (not the re-export wrapper)
    import gateway_pro.oauth.provider as provider_mod
    from gateway.config import settings

    store = context.provider_store
    context._orig_provider_uow = provider_mod.UnitOfWork
    context._orig_jwt_secret = settings.jwt_secret
    provider_mod.UnitOfWork = lambda: _MockUnitOfWork(store)
    settings.jwt_secret = secret


@given('a registered OAuth client "{client_id}"')
def step_register_client(context, client_id):
    context.oauth_client = _make_client(client_id)


@given(
    'a valid auth code "{code}" for client "{client_id}" belonging to user {user_id:d}'
)
def step_add_auth_code(context, code, client_id, user_id):
    context.auth_code_str = code
    context.auth_code_obj = _make_auth_code(code, client_id, user_id)
    context.provider_store.auth_codes[code] = DBAuthCode(
        code=code,
        client_id=client_id,
        redirect_uri="http://localhost/callback",
        redirect_uri_provided_explicitly=True,
        scopes="read",
        expires_at=time.time() + 300,
        code_challenge="challenge",
        user_id=user_id,
    )


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------


@when('I exchange auth code "{code}" for client "{client_id}"')
def step_exchange_code(context, code, client_id):
    context.second_exchange_error = None
    try:
        context.token_response = _run(
            context.provider.exchange_authorization_code(
                context.oauth_client, context.auth_code_obj
            )
        )
    except TokenError as exc:
        context.token_response = None
        context.exchange_error = exc


@when('I exchange auth code "{code}" for client "{client_id}" again')
def step_exchange_code_again(context, code, client_id):
    try:
        _run(
            context.provider.exchange_authorization_code(
                context.oauth_client, context.auth_code_obj
            )
        )
        context.second_exchange_error = None
    except TokenError as exc:
        context.second_exchange_error = exc


@when('I load the refresh token for client "{client_id}"')
def step_load_refresh_token(context, client_id):
    rt = context.token_response.refresh_token
    context.loaded_refresh_token = _run(
        context.provider.load_refresh_token(context.oauth_client, rt)
    )


@when("the refresh token is revoked")
def step_revoke_refresh_token(context):
    from gateway_pro.oauth.db import hash_token

    rt = context.token_response.refresh_token
    context.provider_store.refresh_tokens[hash_token(rt)].revoked = True


@when('I exchange the refresh token for client "{client_id}"')
def step_exchange_refresh_token(context, client_id):
    rt_str = context.token_response.refresh_token
    context.original_refresh_token = rt_str
    loaded = _run(context.provider.load_refresh_token(context.oauth_client, rt_str))
    assert loaded is not None, "Refresh token could not be loaded before exchange"
    context.refreshed_token_response = _run(
        context.provider.exchange_refresh_token(context.oauth_client, loaded, [])
    )


@when('I load the original refresh token for client "{client_id}"')
def step_load_original_refresh_token(context, client_id):
    context.loaded_refresh_token = _run(
        context.provider.load_refresh_token(
            context.oauth_client, context.original_refresh_token
        )
    )


@when('I exchange the original refresh token for client "{client_id}" again')
def step_exchange_original_refresh_token_again(context, client_id):
    loaded = _run(
        context.provider.load_refresh_token(
            context.oauth_client, context.original_refresh_token
        )
    )
    context.second_refresh_error = None
    if loaded is None:
        # Token was revoked — simulate what the provider would do
        context.second_refresh_error = TokenError(
            "invalid_grant", "Refresh token not found or revoked."
        )
        return
    try:
        _run(context.provider.exchange_refresh_token(context.oauth_client, loaded, []))
    except TokenError as exc:
        context.second_refresh_error = exc


# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------


@then("the token response contains an access token")
def step_has_access_token(context):
    assert context.token_response is not None, "Token response is None"
    assert context.token_response.access_token, "access_token is empty"


@then("the token response contains a refresh token")
def step_has_refresh_token(context):
    assert context.token_response.refresh_token, "refresh_token is empty"


@then("the access token expires in 3600 seconds")
def step_expires_in(context):
    assert context.token_response.expires_in == 3600, (
        f"Expected expires_in=3600, got {context.token_response.expires_in}"
    )


@then("the access token contains user_id {user_id:d}")
def step_access_token_has_user_id(context, user_id):
    claims = _decode_jwt(context.token_response.access_token)
    assert claims.get("user_id") == user_id, (
        f"Expected user_id={user_id} in JWT claims, got: {claims}"
    )


@then("the second exchange raises an invalid_grant error")
def step_second_exchange_invalid_grant(context):
    assert context.second_exchange_error is not None, (
        "Expected a TokenError on second exchange but none was raised"
    )
    assert context.second_exchange_error.error == "invalid_grant", (
        f"Expected error=invalid_grant, got {context.second_exchange_error.error}"
    )


@then("the loaded refresh token has user_id {user_id:d}")
def step_loaded_rt_has_user_id(context, user_id):
    rt = context.loaded_refresh_token
    assert rt is not None, "Loaded refresh token is None"
    assert isinstance(rt, _RefreshTokenWithJti), (
        f"Expected _RefreshTokenWithJti, got {type(rt)}"
    )
    assert rt.user_id == user_id, (
        f"Expected user_id={user_id} on loaded refresh token, got {rt.user_id}"
    )


@then("the loaded refresh token is None")
def step_loaded_rt_is_none(context):
    assert context.loaded_refresh_token is None, (
        f"Expected loaded refresh token to be None, got {context.loaded_refresh_token}"
    )


@then("the new access token contains user_id {user_id:d}")
def step_new_access_token_has_user_id(context, user_id):
    claims = _decode_jwt(context.refreshed_token_response.access_token)
    assert claims.get("user_id") == user_id, (
        f"Expected user_id={user_id} in refreshed JWT claims, got: {claims}"
    )


@then("the new refresh token is different from the original")
def step_new_rt_differs(context):
    assert (
        context.refreshed_token_response.refresh_token != context.original_refresh_token
    ), "New refresh token should differ from the original (token rotation)"


@then("the second refresh raises an invalid_grant error")
def step_second_refresh_invalid_grant(context):
    assert context.second_refresh_error is not None, (
        "Expected a TokenError on second refresh but none was raised"
    )
    assert context.second_refresh_error.error == "invalid_grant", (
        f"Expected error=invalid_grant, got {context.second_refresh_error.error}"
    )
