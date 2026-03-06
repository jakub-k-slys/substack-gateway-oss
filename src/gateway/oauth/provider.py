from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastmcp.server.auth.auth import AccessToken, OAuthProvider
from mcp.server.auth.provider import (
    AuthorizationCode,
    AuthorizationParams,
    RefreshToken,
    TokenError,
)
from mcp.server.auth.settings import ClientRegistrationOptions, RevocationOptions
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken
from pydantic import AnyHttpUrl

from gateway.oauth.bearer import _RefreshTokenWithJti
from gateway.oauth.db import (
    DBAccessToken,
    DBAuthRequest,
    DBRefreshToken,
    generate_opaque_token,
    hash_token,
)
from gateway.oauth.repositories import UnitOfWork

_UTC = timezone.utc
_log = logging.getLogger(__name__)

_AUTH_CODE_TTL = 300  # seconds
_ACCESS_TOKEN_TTL = 3600  # seconds
_AUTH_REQUEST_TTL = 600  # seconds


class NeonOAuthProvider(OAuthProvider):
    def __init__(self, base_url: str, login_base_url: str) -> None:
        super().__init__(
            base_url=base_url,
            client_registration_options=ClientRegistrationOptions(enabled=True),
            revocation_options=RevocationOptions(enabled=True),
        )
        self._login_base_url = login_base_url.rstrip("/")

    # ------------------------------------------------------------------
    # OAuthAuthorizationServerProvider interface
    # ------------------------------------------------------------------

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        async with UnitOfWork() as uow:
            record = await uow.oauth_clients.get(client_id)
        if record is None:
            return None
        return OAuthClientInformationFull.model_validate_json(record.client_data)

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        if not client_info.client_id:
            return
        async with UnitOfWork() as uow:
            await uow.oauth_clients.upsert(
                client_info.client_id, client_info.model_dump_json()
            )

    async def authorize(
        self, client: OAuthClientInformationFull, params: AuthorizationParams
    ) -> str:
        request_id = str(uuid.uuid4())
        expires_at = datetime.now(_UTC) + timedelta(seconds=_AUTH_REQUEST_TTL)
        async with UnitOfWork() as uow:
            await uow.auth_requests.save(
                DBAuthRequest(
                    request_id=request_id,
                    client_id=client.client_id,
                    code_challenge=params.code_challenge,
                    redirect_uri=str(params.redirect_uri),
                    redirect_uri_provided_explicitly=params.redirect_uri_provided_explicitly,
                    scopes=" ".join(params.scopes or []),
                    state=params.state,
                    resource=params.resource,
                    expires_at=expires_at,
                )
            )
        return f"{self._login_base_url}/login?request_id={request_id}"

    async def load_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: str
    ) -> AuthorizationCode | None:
        if not client.client_id:
            return None
        async with UnitOfWork() as uow:
            record = await uow.auth_codes.get(authorization_code, client.client_id)
        if record is None:
            return None
        if record.expires_at < time.time():
            return None
        return AuthorizationCode(
            code=record.code,
            client_id=record.client_id,
            redirect_uri=AnyHttpUrl(record.redirect_uri),
            redirect_uri_provided_explicitly=record.redirect_uri_provided_explicitly,
            scopes=record.scopes.split() if record.scopes else [],
            expires_at=record.expires_at,
            code_challenge=record.code_challenge,
            resource=record.resource,
        )

    async def exchange_authorization_code(
        self,
        client: OAuthClientInformationFull,
        authorization_code: AuthorizationCode,
    ) -> OAuthToken:
        if not client.client_id:
            raise TokenError("invalid_client", "Client ID is required.")

        refresh_token_str = generate_opaque_token()
        refresh_hash = hash_token(refresh_token_str)

        async with UnitOfWork() as uow:
            user_id = await uow.auth_codes.consume(authorization_code.code)
            if user_id is None:
                raise TokenError("invalid_grant", "Authorization code already used.")

            access_token_str, jti, exp = self._issue_jwt(
                client.client_id, authorization_code.scopes, user_id
            )
            await uow.access_tokens.save(
                DBAccessToken(
                    jti=jti,
                    client_id=client.client_id,
                    scopes=" ".join(authorization_code.scopes),
                    expires_at=exp,
                )
            )
            await uow.refresh_tokens.save(
                DBRefreshToken(
                    token_hash=refresh_hash,
                    client_id=client.client_id,
                    scopes=" ".join(authorization_code.scopes),
                    access_jti=jti,
                )
            )

        return OAuthToken(
            access_token=access_token_str,
            token_type="Bearer",
            expires_in=_ACCESS_TOKEN_TTL,
            refresh_token=refresh_token_str,
            scope=" ".join(authorization_code.scopes),
        )

    async def load_refresh_token(
        self, client: OAuthClientInformationFull, refresh_token: str
    ) -> RefreshToken | None:
        if not client.client_id:
            return None
        token_hash = hash_token(refresh_token)
        async with UnitOfWork() as uow:
            record = await uow.refresh_tokens.get_active(token_hash, client.client_id)
        if record is None:
            return None
        if record.expires_at is not None and record.expires_at < time.time():
            return None
        return _RefreshTokenWithJti(
            token=refresh_token,
            client_id=record.client_id,
            scopes=record.scopes.split() if record.scopes else [],
            expires_at=record.expires_at,
            access_jti=record.access_jti,
        )

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: RefreshToken,
        scopes: list[str],
    ) -> OAuthToken:
        if scopes and not set(scopes).issubset(set(refresh_token.scopes)):
            raise TokenError(
                "invalid_scope", "Requested scopes exceed authorized scopes."
            )
        if not client.client_id:
            raise TokenError("invalid_client", "Client ID is required.")
        effective_scopes = scopes if scopes else list(refresh_token.scopes)

        old_hash = hash_token(refresh_token.token)
        old_jti = getattr(refresh_token, "access_jti", None)
        new_refresh_str = generate_opaque_token()
        new_refresh_hash = hash_token(new_refresh_str)

        async with UnitOfWork() as uow:
            await uow.refresh_tokens.revoke(old_hash)
            if old_jti:
                await uow.access_tokens.revoke(old_jti)

            access_token_str, jti, exp = self._issue_jwt(
                client.client_id, effective_scopes
            )
            await uow.access_tokens.save(
                DBAccessToken(
                    jti=jti,
                    client_id=client.client_id,
                    scopes=" ".join(effective_scopes),
                    expires_at=exp,
                )
            )
            await uow.refresh_tokens.save(
                DBRefreshToken(
                    token_hash=new_refresh_hash,
                    client_id=client.client_id,
                    scopes=" ".join(effective_scopes),
                    access_jti=jti,
                )
            )

        return OAuthToken(
            access_token=access_token_str,
            token_type="Bearer",
            expires_in=_ACCESS_TOKEN_TTL,
            refresh_token=new_refresh_str,
            scope=" ".join(effective_scopes),
        )

    async def load_access_token(self, token: str) -> AccessToken | None:
        from gateway.config import settings

        if not settings.jwt_secret:
            return None
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        except jwt.PyJWTError:
            return None

        jti = payload.get("jti")
        if not jti:
            return None

        async with UnitOfWork() as uow:
            record = await uow.access_tokens.get(jti)
        if record is None or record.revoked:
            return None

        scope_str = payload.get("scope", "")
        return AccessToken(
            token=token,
            client_id=payload.get("client_id", payload.get("sub", "")),
            scopes=scope_str.split() if scope_str else [],
            expires_at=payload.get("exp"),
            claims=payload,
        )

    async def revoke_token(self, token: AccessToken | RefreshToken) -> None:
        if isinstance(token, AccessToken):
            from gateway.config import settings

            if not settings.jwt_secret:
                return
            try:
                payload = jwt.decode(
                    token.token, settings.jwt_secret, algorithms=["HS256"]
                )
            except jwt.PyJWTError:
                return
            jti = payload.get("jti")
            if not jti:
                return
            async with UnitOfWork() as uow:
                await uow.access_tokens.revoke(jti)
        else:
            token_hash = hash_token(token.token)
            async with UnitOfWork() as uow:
                rt = await uow.refresh_tokens.get(token_hash)
                if rt:
                    if rt.access_jti:
                        await uow.access_tokens.revoke(rt.access_jti)
                    await uow.refresh_tokens.revoke(token_hash)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _issue_jwt(
        self,
        client_id: str,
        scopes: list[str],
        user_id: int | None = None,
    ) -> tuple[str, str, int]:
        from gateway.config import settings

        assert settings.jwt_secret, "JWT_SECRET must be configured"
        jti = str(uuid.uuid4())
        now = int(time.time())
        exp = now + _ACCESS_TOKEN_TTL
        payload: dict[str, Any] = {
            "jti": jti,
            "sub": client_id,
            "iat": now,
            "exp": exp,
            "scope": " ".join(scopes),
            "client_id": client_id,
        }
        if user_id is not None:
            payload["user_id"] = user_id
        token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
        return token, jti, exp
