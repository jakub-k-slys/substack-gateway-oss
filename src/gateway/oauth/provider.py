from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime, timedelta, timezone
from functools import partial
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
from sqlalchemy import delete, insert, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from starlette.routing import Route

from gateway.oauth.bearer import _RefreshTokenWithJti
from gateway.oauth.db import (
    generate_opaque_token,
    get_engine,
    hash_token,
    t_access_tokens,
    t_auth_codes,
    t_auth_requests,
    t_oauth_clients,
    t_refresh_tokens,
)
from gateway.oauth.login import handle_login, handle_token_form

_UTC = timezone.utc
_log = logging.getLogger(__name__)

_AUTH_CODE_TTL = 300  # seconds
_ACCESS_TOKEN_TTL = 3600  # seconds
_AUTH_REQUEST_TTL = 600  # seconds


class NeonOAuthProvider(OAuthProvider):
    def __init__(self, base_url: str) -> None:
        super().__init__(
            base_url=base_url,
            client_registration_options=ClientRegistrationOptions(enabled=True),
            revocation_options=RevocationOptions(enabled=True),
        )

    # ------------------------------------------------------------------
    # OAuthAuthorizationServerProvider interface
    # ------------------------------------------------------------------

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        async with get_engine().connect() as conn:
            row = await conn.execute(
                select(t_oauth_clients.c.client_data).where(
                    t_oauth_clients.c.client_id == client_id
                )
            )
            record = row.fetchone()
        if record is None:
            return None
        return OAuthClientInformationFull.model_validate_json(record[0])

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        stmt = pg_insert(t_oauth_clients).values(
            client_id=client_info.client_id,
            client_data=client_info.model_dump_json(),
        )
        async with get_engine().begin() as conn:
            await conn.execute(
                stmt.on_conflict_do_update(
                    index_elements=["client_id"],
                    set_={"client_data": stmt.excluded.client_data},
                )
            )

    async def authorize(
        self, client: OAuthClientInformationFull, params: AuthorizationParams
    ) -> str:
        request_id = str(uuid.uuid4())
        expires_at = datetime.now(_UTC) + timedelta(seconds=_AUTH_REQUEST_TTL)
        scopes_str = " ".join(params.scopes or [])
        async with get_engine().begin() as conn:
            await conn.execute(
                insert(t_auth_requests).values(
                    request_id=request_id,
                    client_id=client.client_id,
                    code_challenge=params.code_challenge,
                    redirect_uri=str(params.redirect_uri),
                    redirect_uri_provided_explicitly=params.redirect_uri_provided_explicitly,
                    scopes=scopes_str,
                    state=params.state,
                    resource=params.resource,
                    expires_at=expires_at,
                )
            )
        return f"{str(self.base_url).rstrip('/')}/login?request_id={request_id}"

    async def load_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: str
    ) -> AuthorizationCode | None:
        async with get_engine().connect() as conn:
            row = await conn.execute(
                select(
                    t_auth_codes.c.code,
                    t_auth_codes.c.client_id,
                    t_auth_codes.c.redirect_uri,
                    t_auth_codes.c.redirect_uri_provided_explicitly,
                    t_auth_codes.c.scopes,
                    t_auth_codes.c.expires_at,
                    t_auth_codes.c.code_challenge,
                    t_auth_codes.c.resource,
                ).where(
                    (t_auth_codes.c.code == authorization_code)
                    & (t_auth_codes.c.client_id == client.client_id)
                )
            )
            record = row.fetchone()
        if record is None:
            return None
        code, cid, ruri, ruri_ex, scopes_str, expires_at, challenge, resource = record
        if expires_at < time.time():
            return None
        return AuthorizationCode(
            code=code,
            client_id=cid,
            redirect_uri=AnyHttpUrl(ruri),
            redirect_uri_provided_explicitly=ruri_ex,
            scopes=(scopes_str.split() if scopes_str else []),
            expires_at=expires_at,
            code_challenge=challenge,
            resource=resource,
        )

    async def exchange_authorization_code(
        self,
        client: OAuthClientInformationFull,
        authorization_code: AuthorizationCode,
    ) -> OAuthToken:
        if not client.client_id:
            raise TokenError("invalid_client", "Client ID is required.")

        async with get_engine().begin() as conn:
            deleted = await conn.execute(
                delete(t_auth_codes)
                .where(t_auth_codes.c.code == authorization_code.code)
                .returning(t_auth_codes.c.code, t_auth_codes.c.user_id)
            )
            row = deleted.fetchone()
            if row is None:
                raise TokenError("invalid_grant", "Authorization code already used.")
            user_id: int | None = row[1]

        access_token_str, jti, exp = self._issue_jwt(
            client.client_id, authorization_code.scopes, user_id
        )
        refresh_token_str = generate_opaque_token()
        refresh_hash = hash_token(refresh_token_str)

        async with get_engine().begin() as conn:
            await conn.execute(
                insert(t_access_tokens).values(
                    jti=jti,
                    client_id=client.client_id,
                    scopes=" ".join(authorization_code.scopes),
                    expires_at=exp,
                )
            )
            await conn.execute(
                insert(t_refresh_tokens).values(
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
        token_hash = hash_token(refresh_token)
        async with get_engine().connect() as conn:
            row = await conn.execute(
                select(
                    t_refresh_tokens.c.client_id,
                    t_refresh_tokens.c.scopes,
                    t_refresh_tokens.c.expires_at,
                    t_refresh_tokens.c.access_jti,
                ).where(
                    (t_refresh_tokens.c.token_hash == token_hash)
                    & (t_refresh_tokens.c.client_id == client.client_id)
                    & (t_refresh_tokens.c.revoked.is_(False))
                )
            )
            record = row.fetchone()
        if record is None:
            return None
        cid, scopes_str, expires_at, access_jti = record
        if expires_at is not None and expires_at < time.time():
            return None
        return _RefreshTokenWithJti(
            token=refresh_token,
            client_id=cid,
            scopes=(scopes_str.split() if scopes_str else []),
            expires_at=expires_at,
            access_jti=access_jti,
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

        async with get_engine().begin() as conn:
            await conn.execute(
                update(t_refresh_tokens)
                .where(t_refresh_tokens.c.token_hash == old_hash)
                .values(revoked=True)
            )
            if old_jti:
                await conn.execute(
                    update(t_access_tokens)
                    .where(t_access_tokens.c.jti == old_jti)
                    .values(revoked=True)
                )

        access_token_str, jti, exp = self._issue_jwt(client.client_id, effective_scopes)
        new_refresh_str = generate_opaque_token()
        new_refresh_hash = hash_token(new_refresh_str)

        async with get_engine().begin() as conn:
            await conn.execute(
                insert(t_access_tokens).values(
                    jti=jti,
                    client_id=client.client_id,
                    scopes=" ".join(effective_scopes),
                    expires_at=exp,
                )
            )
            await conn.execute(
                insert(t_refresh_tokens).values(
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

        async with get_engine().connect() as conn:
            row = await conn.execute(
                select(t_access_tokens.c.jti).where(
                    (t_access_tokens.c.jti == jti)
                    & (t_access_tokens.c.revoked.is_(False))
                )
            )
            if row.fetchone() is None:
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
        async with get_engine().begin() as conn:
            if isinstance(token, AccessToken):
                from gateway.config import settings

                if not settings.jwt_secret:
                    return
                try:
                    payload = jwt.decode(
                        token.token, settings.jwt_secret, algorithms=["HS256"]
                    )
                    jti = payload.get("jti")
                    if jti:
                        await conn.execute(
                            update(t_access_tokens)
                            .where(t_access_tokens.c.jti == jti)
                            .values(revoked=True)
                        )
                except jwt.PyJWTError:
                    pass
            else:
                token_hash = hash_token(token.token)
                row = await conn.execute(
                    select(t_refresh_tokens.c.access_jti).where(
                        t_refresh_tokens.c.token_hash == token_hash
                    )
                )
                record = row.fetchone()
                if record and record[0]:
                    await conn.execute(
                        update(t_access_tokens)
                        .where(t_access_tokens.c.jti == record[0])
                        .values(revoked=True)
                    )
                await conn.execute(
                    update(t_refresh_tokens)
                    .where(t_refresh_tokens.c.token_hash == token_hash)
                    .values(revoked=True)
                )

    # ------------------------------------------------------------------
    # Login routes (two-phase)
    # ------------------------------------------------------------------

    def get_routes(self, mcp_path: str | None = None) -> list[Any]:
        routes = super().get_routes(mcp_path)
        base_url = str(self.base_url)
        routes.append(
            Route(
                "/login",
                endpoint=partial(handle_login, base_url=base_url),
                methods=["GET", "POST"],
            )
        )
        routes.append(
            Route(
                "/login/token",
                endpoint=handle_token_form,
                methods=["GET", "POST"],
            )
        )
        return routes

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
