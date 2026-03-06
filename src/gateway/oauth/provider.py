from __future__ import annotations

import html as _html
import logging
import secrets
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt
from fastmcp.server.auth.auth import AccessToken, OAuthProvider
from mcp.server.auth.provider import (
    AuthorizationCode,
    AuthorizationParams,
    RefreshToken,
    TokenError,
    construct_redirect_uri,
)
from mcp.server.auth.settings import ClientRegistrationOptions, RevocationOptions
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken
from pydantic import AnyHttpUrl
from sqlalchemy import text
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette.routing import Route

from gateway.oauth.db import generate_opaque_token, get_engine, hash_token

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
                text("SELECT client_data FROM oauth_clients WHERE client_id = :id"),
                {"id": client_id},
            )
            record = row.fetchone()
        if record is None:
            return None
        return OAuthClientInformationFull.model_validate_json(record[0])

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        async with get_engine().begin() as conn:
            await conn.execute(
                text(
                    "INSERT INTO oauth_clients (client_id, client_data) "
                    "VALUES (:id, :data) "
                    "ON CONFLICT (client_id) DO UPDATE SET client_data = :data"
                ),
                {
                    "id": client_info.client_id,
                    "data": client_info.model_dump_json(),
                },
            )

    async def authorize(
        self, client: OAuthClientInformationFull, params: AuthorizationParams
    ) -> str:
        request_id = str(uuid.uuid4())
        expires_at = datetime.now(_UTC) + timedelta(seconds=_AUTH_REQUEST_TTL)
        scopes_str = " ".join(params.scopes or [])
        async with get_engine().begin() as conn:
            await conn.execute(
                text(
                    "INSERT INTO auth_requests "
                    "(request_id, client_id, code_challenge, redirect_uri, "
                    "redirect_uri_provided_explicitly, scopes, state, resource, expires_at) "
                    "VALUES (:rid, :cid, :cc, :ruri, :ruri_ex, :scopes, :state, :resource, :exp)"
                ),
                {
                    "rid": request_id,
                    "cid": client.client_id,
                    "cc": params.code_challenge,
                    "ruri": str(params.redirect_uri),
                    "ruri_ex": params.redirect_uri_provided_explicitly,
                    "scopes": scopes_str,
                    "state": params.state,
                    "resource": params.resource,
                    "exp": expires_at,
                },
            )
        login_url = f"{str(self.base_url).rstrip('/')}/login?request_id={request_id}"
        return login_url

    async def load_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: str
    ) -> AuthorizationCode | None:
        async with get_engine().connect() as conn:
            row = await conn.execute(
                text(
                    "SELECT code, client_id, redirect_uri, redirect_uri_provided_explicitly, "
                    "scopes, expires_at, code_challenge, resource "
                    "FROM auth_codes WHERE code = :code AND client_id = :cid"
                ),
                {"code": authorization_code, "cid": client.client_id},
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
        # Consume the auth code (single-use)
        async with get_engine().begin() as conn:
            deleted = await conn.execute(
                text("DELETE FROM auth_codes WHERE code = :code RETURNING code"),
                {"code": authorization_code.code},
            )
            if deleted.fetchone() is None:
                raise TokenError("invalid_grant", "Authorization code already used.")

        if not client.client_id:
            raise TokenError("invalid_client", "Client ID is required.")
        access_token_str, jti, exp = self._issue_jwt(
            client.client_id, authorization_code.scopes
        )
        refresh_token_str = generate_opaque_token()
        refresh_hash = hash_token(refresh_token_str)

        async with get_engine().begin() as conn:
            await conn.execute(
                text(
                    "INSERT INTO access_tokens (jti, client_id, scopes, expires_at) "
                    "VALUES (:jti, :cid, :scopes, :exp)"
                ),
                {
                    "jti": jti,
                    "cid": client.client_id,
                    "scopes": " ".join(authorization_code.scopes),
                    "exp": exp,
                },
            )
            await conn.execute(
                text(
                    "INSERT INTO refresh_tokens "
                    "(token_hash, client_id, scopes, access_jti) "
                    "VALUES (:h, :cid, :scopes, :jti)"
                ),
                {
                    "h": refresh_hash,
                    "cid": client.client_id,
                    "scopes": " ".join(authorization_code.scopes),
                    "jti": jti,
                },
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
                text(
                    "SELECT client_id, scopes, expires_at, access_jti "
                    "FROM refresh_tokens "
                    "WHERE token_hash = :h AND client_id = :cid AND revoked = FALSE"
                ),
                {"h": token_hash, "cid": client.client_id},
            )
            record = row.fetchone()
        if record is None:
            return None
        cid, scopes_str, expires_at, access_jti = record
        if expires_at is not None and expires_at < time.time():
            return None
        rt = _RefreshTokenWithJti(
            token=refresh_token,
            client_id=cid,
            scopes=(scopes_str.split() if scopes_str else []),
            expires_at=expires_at,
            access_jti=access_jti,
        )
        return rt

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
        effective_scopes = scopes if scopes else list(refresh_token.scopes)

        old_hash = hash_token(refresh_token.token)
        old_jti = getattr(refresh_token, "access_jti", None)

        async with get_engine().begin() as conn:
            await conn.execute(
                text("UPDATE refresh_tokens SET revoked = TRUE WHERE token_hash = :h"),
                {"h": old_hash},
            )
            if old_jti:
                await conn.execute(
                    text("UPDATE access_tokens SET revoked = TRUE WHERE jti = :jti"),
                    {"jti": old_jti},
                )

        if not client.client_id:
            raise TokenError("invalid_client", "Client ID is required.")
        access_token_str, jti, exp = self._issue_jwt(client.client_id, effective_scopes)
        new_refresh_str = generate_opaque_token()
        new_refresh_hash = hash_token(new_refresh_str)

        async with get_engine().begin() as conn:
            await conn.execute(
                text(
                    "INSERT INTO access_tokens (jti, client_id, scopes, expires_at) "
                    "VALUES (:jti, :cid, :scopes, :exp)"
                ),
                {
                    "jti": jti,
                    "cid": client.client_id,
                    "scopes": " ".join(effective_scopes),
                    "exp": exp,
                },
            )
            await conn.execute(
                text(
                    "INSERT INTO refresh_tokens "
                    "(token_hash, client_id, scopes, access_jti) "
                    "VALUES (:h, :cid, :scopes, :jti)"
                ),
                {
                    "h": new_refresh_hash,
                    "cid": client.client_id,
                    "scopes": " ".join(effective_scopes),
                    "jti": jti,
                },
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
                text(
                    "SELECT jti FROM access_tokens WHERE jti = :jti AND revoked = FALSE"
                ),
                {"jti": jti},
            )
            if row.fetchone() is None:
                return None

        scope_str = payload.get("scope", "")
        return AccessToken(
            token=token,
            client_id=payload.get("client_id", payload.get("sub", "")),
            scopes=scope_str.split() if scope_str else [],
            expires_at=payload.get("exp"),
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
                            text(
                                "UPDATE access_tokens SET revoked = TRUE "
                                "WHERE jti = :jti"
                            ),
                            {"jti": jti},
                        )
                except jwt.PyJWTError:
                    pass
            else:
                token_hash = hash_token(token.token)
                row = await conn.execute(
                    text("SELECT access_jti FROM refresh_tokens WHERE token_hash = :h"),
                    {"h": token_hash},
                )
                record = row.fetchone()
                if record and record[0]:
                    await conn.execute(
                        text(
                            "UPDATE access_tokens SET revoked = TRUE WHERE jti = :jti"
                        ),
                        {"jti": record[0]},
                    )
                await conn.execute(
                    text(
                        "UPDATE refresh_tokens SET revoked = TRUE WHERE token_hash = :h"
                    ),
                    {"h": token_hash},
                )

    # ------------------------------------------------------------------
    # Login route (injected into OAuth routes)
    # ------------------------------------------------------------------

    def get_routes(self, mcp_path: str | None = None) -> list[Any]:
        routes = super().get_routes(mcp_path)
        routes.append(
            Route("/login", endpoint=self._handle_login, methods=["GET", "POST"])
        )
        return routes

    async def _handle_login(self, request: Request) -> Response:
        if request.method == "GET":
            return self._render_form(request.query_params.get("request_id", ""))
        return await self._process_login(request)

    def _render_form(self, request_id: str, error: str = "") -> Response:
        safe_rid = _html.escape(request_id)
        safe_err = f'<p class="error">{_html.escape(error)}</p>' if error else ""
        return HTMLResponse(_LOGIN_HTML.format(request_id=safe_rid, error=safe_err))

    async def _process_login(self, request: Request) -> Response:
        form = await request.form()
        request_id = str(form.get("request_id", "")).strip()
        email = str(form.get("email", "")).strip().lower()
        password = str(form.get("password", ""))

        if not (request_id and email and password):
            return self._render_form(request_id, "All fields are required.")

        # Load the pending auth request
        async with get_engine().connect() as conn:
            row = await conn.execute(
                text(
                    "SELECT client_id, code_challenge, redirect_uri, "
                    "redirect_uri_provided_explicitly, scopes, state, "
                    "resource, expires_at "
                    "FROM auth_requests WHERE request_id = :rid"
                ),
                {"rid": request_id},
            )
            rec = row.fetchone()

        if rec is None:
            return self._render_form(request_id, "Session expired. Please try again.")

        (
            cid,
            code_challenge,
            redirect_uri,
            ruri_ex,
            scopes_str,
            state,
            resource,
            expires_at,
        ) = rec

        # Make expires_at timezone-aware if needed
        if hasattr(expires_at, "tzinfo") and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=_UTC)
        if datetime.now(_UTC) > expires_at:
            return self._render_form(request_id, "Session expired. Please try again.")

        # Verify credentials
        async with get_engine().connect() as conn:
            row = await conn.execute(
                text("SELECT hashed_password FROM users WHERE email = :email"),
                {"email": email},
            )
            user_rec = row.fetchone()

        if user_rec is None or not bcrypt.checkpw(
            password.encode(), user_rec[0].encode()
        ):
            return self._render_form(request_id, "Invalid email or password.")

        # Issue auth code
        code = secrets.token_urlsafe(32)
        exp = time.time() + _AUTH_CODE_TTL

        async with get_engine().begin() as conn:
            await conn.execute(
                text(
                    "INSERT INTO auth_codes "
                    "(code, client_id, redirect_uri, redirect_uri_provided_explicitly, "
                    "scopes, expires_at, code_challenge, resource) "
                    "VALUES (:code, :cid, :ruri, :ruri_ex, :scopes, :exp, :cc, :resource)"
                ),
                {
                    "code": code,
                    "cid": cid,
                    "ruri": redirect_uri,
                    "ruri_ex": ruri_ex,
                    "scopes": scopes_str,
                    "exp": exp,
                    "cc": code_challenge,
                    "resource": resource,
                },
            )
            await conn.execute(
                text("DELETE FROM auth_requests WHERE request_id = :rid"),
                {"rid": request_id},
            )

        redirect_url = construct_redirect_uri(redirect_uri, code=code, state=state)
        return RedirectResponse(url=redirect_url, status_code=302)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _issue_jwt(self, client_id: str, scopes: list[str]) -> tuple[str, str, int]:
        from gateway.config import settings

        assert settings.jwt_secret, "JWT_SECRET must be configured"
        jti = str(uuid.uuid4())
        now = int(time.time())
        exp = now + _ACCESS_TOKEN_TTL
        payload = {
            "jti": jti,
            "sub": client_id,
            "iat": now,
            "exp": exp,
            "scope": " ".join(scopes),
            "client_id": client_id,
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
        return token, jti, exp


class _RefreshTokenWithJti(RefreshToken):
    """RefreshToken extended with access_jti for cascade revocation."""

    access_jti: str | None = None


# ------------------------------------------------------------------
# Login page HTML
# ------------------------------------------------------------------

_LOGIN_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Substack Gateway — Sign in</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #f5f5f0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .card {{
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,.08);
      padding: 40px 36px;
      width: 100%;
      max-width: 380px;
    }}
    h1 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; color: #111; }}
    .sub {{ font-size: .9rem; color: #666; margin-bottom: 28px; }}
    label {{ display: block; font-size: .85rem; font-weight: 600; color: #333; margin-bottom: 6px; }}
    input[type=email], input[type=password] {{
      width: 100%; padding: 10px 12px;
      border: 1.5px solid #ddd; border-radius: 8px;
      font-size: .95rem; outline: none; margin-bottom: 18px;
      transition: border-color .15s;
    }}
    input:focus {{ border-color: #ff6719; }}
    button {{
      width: 100%; padding: 11px;
      background: #ff6719; color: #fff;
      border: none; border-radius: 8px;
      font-size: 1rem; font-weight: 600; cursor: pointer;
      transition: background .15s;
    }}
    button:hover {{ background: #e55c12; }}
    .error {{
      color: #c0392b; font-size: .88rem; margin-bottom: 16px;
      padding: 10px 12px; background: #fdf3f3;
      border-radius: 6px; border: 1px solid #f5c6cb;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Substack Gateway</h1>
    <p class="sub">Sign in to continue</p>
    {error}
    <form method="post">
      <input type="hidden" name="request_id" value="{request_id}">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required autofocus
             placeholder="you@example.com">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required
             placeholder="••••••••">
      <button type="submit">Sign in</button>
    </form>
  </div>
</body>
</html>
"""
