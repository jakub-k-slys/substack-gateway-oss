from __future__ import annotations

import base64
import html as _html
import json
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
_LOGIN_SESSION_TTL = 600  # seconds between phase-1 and phase-2


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
        return f"{str(self.base_url).rstrip('/')}/login?request_id={request_id}"

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
        if not client.client_id:
            raise TokenError("invalid_client", "Client ID is required.")

        # Consume the auth code and retrieve the user_id stored in it
        async with get_engine().begin() as conn:
            deleted = await conn.execute(
                text(
                    "DELETE FROM auth_codes WHERE code = :code RETURNING code, user_id"
                ),
                {"code": authorization_code.code},
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
                text("UPDATE refresh_tokens SET revoked = TRUE WHERE token_hash = :h"),
                {"h": old_hash},
            )
            if old_jti:
                await conn.execute(
                    text("UPDATE access_tokens SET revoked = TRUE WHERE jti = :jti"),
                    {"jti": old_jti},
                )

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
    # Login routes (two-phase)
    # ------------------------------------------------------------------

    def get_routes(self, mcp_path: str | None = None) -> list[Any]:
        routes = super().get_routes(mcp_path)
        routes.append(
            Route("/login", endpoint=self._handle_login, methods=["GET", "POST"])
        )
        routes.append(
            Route(
                "/login/token",
                endpoint=self._handle_token_form,
                methods=["GET", "POST"],
            )
        )
        return routes

    # Phase 1 — email + password

    async def _handle_login(self, request: Request) -> Response:
        if request.method == "GET":
            return self._render_login(request.query_params.get("request_id", ""))
        return await self._process_login(request)

    def _render_login(self, request_id: str, error: str = "") -> Response:
        safe_rid = _html.escape(request_id)
        safe_err = f'<p class="error">{_html.escape(error)}</p>' if error else ""
        return HTMLResponse(_LOGIN_HTML.format(request_id=safe_rid, error=safe_err))

    async def _process_login(self, request: Request) -> Response:
        form = await request.form()
        request_id = str(form.get("request_id", "")).strip()
        email = str(form.get("email", "")).strip().lower()
        password = str(form.get("password", ""))

        if not (request_id and email and password):
            return self._render_login(request_id, "All fields are required.")

        # Validate the OAuth request still exists and hasn't expired
        async with get_engine().connect() as conn:
            row = await conn.execute(
                text("SELECT expires_at FROM auth_requests WHERE request_id = :rid"),
                {"rid": request_id},
            )
            rec = row.fetchone()

        if rec is None:
            return self._render_login(request_id, "Session expired. Please try again.")
        expires_at = rec[0]
        if hasattr(expires_at, "tzinfo") and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=_UTC)
        if datetime.now(_UTC) > expires_at:
            return self._render_login(request_id, "Session expired. Please try again.")

        # Verify credentials
        async with get_engine().connect() as conn:
            row = await conn.execute(
                text("SELECT id, hashed_password FROM users WHERE email = :email"),
                {"email": email},
            )
            user_rec = row.fetchone()

        if user_rec is None or not bcrypt.checkpw(
            password.encode(), user_rec[1].encode()
        ):
            return self._render_login(request_id, "Invalid email or password.")

        user_id: int = user_rec[0]

        # Create a login session linking this OAuth request to the authenticated user
        session_id = str(uuid.uuid4())
        session_expires = datetime.now(_UTC) + timedelta(seconds=_LOGIN_SESSION_TTL)
        async with get_engine().begin() as conn:
            await conn.execute(
                text(
                    "INSERT INTO login_sessions "
                    "(session_id, request_id, user_id, expires_at) "
                    "VALUES (:sid, :rid, :uid, :exp)"
                ),
                {
                    "sid": session_id,
                    "rid": request_id,
                    "uid": user_id,
                    "exp": session_expires,
                },
            )

        redirect = (
            f"{str(self.base_url).rstrip('/')}/login/token?session_id={session_id}"
        )
        return RedirectResponse(url=redirect, status_code=302)

    # Phase 2 — Substack bearer token

    async def _handle_token_form(self, request: Request) -> Response:
        if request.method == "GET":
            return self._render_token_form(request.query_params.get("session_id", ""))
        return await self._process_token_form(request)

    def _render_token_form(self, session_id: str, error: str = "") -> Response:
        safe_sid = _html.escape(session_id)
        safe_err = f'<p class="error">{_html.escape(error)}</p>' if error else ""
        return HTMLResponse(_TOKEN_HTML.format(session_id=safe_sid, error=safe_err))

    async def _process_token_form(self, request: Request) -> Response:
        form = await request.form()
        session_id = str(form.get("session_id", "")).strip()
        substack_sid = str(form.get("substack_sid", "")).strip()
        connect_sid = str(form.get("connect_sid", "")).strip()
        pub_url = str(form.get("pub_url", "")).strip().rstrip("/")

        if not (session_id and substack_sid and connect_sid and pub_url):
            return self._render_token_form(session_id, "All fields are required.")

        # Load and validate the login session
        async with get_engine().connect() as conn:
            row = await conn.execute(
                text(
                    "SELECT request_id, user_id, expires_at "
                    "FROM login_sessions WHERE session_id = :sid"
                ),
                {"sid": session_id},
            )
            sess = row.fetchone()

        if sess is None:
            return self._render_token_form(
                session_id, "Session expired. Please start over."
            )
        request_id, user_id, sess_expires = sess
        if hasattr(sess_expires, "tzinfo") and sess_expires.tzinfo is None:
            sess_expires = sess_expires.replace(tzinfo=_UTC)
        if datetime.now(_UTC) > sess_expires:
            return self._render_token_form(
                session_id, "Session expired. Please start over."
            )

        # Load the original OAuth request
        async with get_engine().connect() as conn:
            row = await conn.execute(
                text(
                    "SELECT client_id, code_challenge, redirect_uri, "
                    "redirect_uri_provided_explicitly, scopes, state, resource "
                    "FROM auth_requests WHERE request_id = :rid"
                ),
                {"rid": request_id},
            )
            auth_req = row.fetchone()

        if auth_req is None:
            return self._render_token_form(
                session_id, "OAuth session expired. Please start over."
            )
        cid, code_challenge, redirect_uri, ruri_ex, scopes_str, state, resource = (
            auth_req
        )

        # Build and validate the bearer token from the provided cookie values
        bearer = _encode_bearer(substack_sid, connect_sid)
        try:
            _validate_bearer(bearer)
        except ValueError as exc:
            return self._render_token_form(session_id, str(exc))

        # Persist the user's Substack credentials
        async with get_engine().begin() as conn:
            await conn.execute(
                text(
                    "INSERT INTO user_credentials (user_id, bearer, pub_url) "
                    "VALUES (:uid, :bearer, :pub_url) "
                    "ON CONFLICT (user_id) DO UPDATE "
                    "SET bearer = :bearer, pub_url = :pub_url, updated_at = NOW()"
                ),
                {"uid": user_id, "bearer": bearer, "pub_url": pub_url},
            )

        # Issue the auth code, embedding user_id for later JWT issuance
        code = secrets.token_urlsafe(32)
        exp = time.time() + _AUTH_CODE_TTL

        async with get_engine().begin() as conn:
            await conn.execute(
                text(
                    "INSERT INTO auth_codes "
                    "(code, client_id, redirect_uri, redirect_uri_provided_explicitly, "
                    "scopes, expires_at, code_challenge, resource, user_id) "
                    "VALUES (:code, :cid, :ruri, :ruri_ex, :scopes, :exp, :cc, :resource, :uid)"
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
                    "uid": user_id,
                },
            )
            # Clean up transient rows
            await conn.execute(
                text("DELETE FROM login_sessions WHERE session_id = :sid"),
                {"sid": session_id},
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


class _RefreshTokenWithJti(RefreshToken):
    """RefreshToken extended with access_jti for cascade revocation."""

    access_jti: str | None = None


# ------------------------------------------------------------------
# Bearer token helpers
# ------------------------------------------------------------------


def _encode_bearer(substack_sid: str, connect_sid: str) -> str:
    """Encode Substack cookie values into the base64 bearer token format."""
    payload = {"substack_sid": substack_sid, "connect_sid": connect_sid}
    return base64.b64encode(json.dumps(payload).encode()).decode()


def _validate_bearer(bearer: str) -> None:
    """Raise ValueError if the bearer token cannot be decoded correctly."""
    try:
        decoded = json.loads(base64.b64decode(bearer.encode()))
    except Exception as exc:
        raise ValueError("Could not decode bearer token.") from exc
    for field in ("substack_sid", "connect_sid"):
        if not decoded.get(field):
            raise ValueError(f"Missing required field: {field}")


# ------------------------------------------------------------------
# Login page HTML — phase 1: email + password
# ------------------------------------------------------------------

_LOGIN_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Substack Gateway — Sign in (1/2)</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #f5f5f0; min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
    }}
    .card {{
      background: #fff; border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,.08);
      padding: 40px 36px; width: 100%; max-width: 380px;
    }}
    .step {{ font-size: .78rem; color: #999; font-weight: 600;
             letter-spacing: .05em; text-transform: uppercase; margin-bottom: 6px; }}
    h1 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; color: #111; }}
    .sub {{ font-size: .9rem; color: #666; margin-bottom: 28px; }}
    label {{ display: block; font-size: .85rem; font-weight: 600;
             color: #333; margin-bottom: 6px; }}
    input[type=email], input[type=password] {{
      width: 100%; padding: 10px 12px;
      border: 1.5px solid #ddd; border-radius: 8px;
      font-size: .95rem; outline: none; margin-bottom: 18px;
      transition: border-color .15s;
    }}
    input:focus {{ border-color: #ff6719; }}
    button {{
      width: 100%; padding: 11px; background: #ff6719; color: #fff;
      border: none; border-radius: 8px; font-size: 1rem;
      font-weight: 600; cursor: pointer; transition: background .15s;
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
    <p class="step">Step 1 of 2</p>
    <h1>Substack Gateway</h1>
    <p class="sub">Sign in with your account credentials</p>
    {error}
    <form method="post">
      <input type="hidden" name="request_id" value="{request_id}">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required autofocus
             placeholder="you@example.com">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required
             placeholder="••••••••">
      <button type="submit">Continue →</button>
    </form>
  </div>
</body>
</html>
"""

# ------------------------------------------------------------------
# Login page HTML — phase 2: Substack bearer token
# ------------------------------------------------------------------

_TOKEN_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Substack Gateway — Connect Substack (2/2)</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #f5f5f0; min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
    }}
    .card {{
      background: #fff; border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,.08);
      padding: 40px 36px; width: 100%; max-width: 420px;
    }}
    .step {{ font-size: .78rem; color: #999; font-weight: 600;
             letter-spacing: .05em; text-transform: uppercase; margin-bottom: 6px; }}
    h1 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; color: #111; }}
    .sub {{ font-size: .9rem; color: #666; margin-bottom: 28px; }}
    label {{ display: block; font-size: .85rem; font-weight: 600;
             color: #333; margin-bottom: 6px; }}
    .hint {{ font-size: .78rem; color: #888; margin-top: -12px; margin-bottom: 16px; }}
    input[type=text], input[type=url], input[type=password] {{
      width: 100%; padding: 10px 12px;
      border: 1.5px solid #ddd; border-radius: 8px;
      font-size: .95rem; outline: none; margin-bottom: 6px;
      transition: border-color .15s; font-family: monospace;
    }}
    input[type=url] {{ font-family: inherit; margin-bottom: 6px; }}
    input:focus {{ border-color: #ff6719; }}
    button {{
      width: 100%; padding: 11px; background: #ff6719; color: #fff;
      border: none; border-radius: 8px; font-size: 1rem;
      font-weight: 600; cursor: pointer; transition: background .15s;
      margin-top: 12px;
    }}
    button:hover {{ background: #e55c12; }}
    .error {{
      color: #c0392b; font-size: .88rem; margin-bottom: 16px;
      padding: 10px 12px; background: #fdf3f3;
      border-radius: 6px; border: 1px solid #f5c6cb;
    }}
    details {{ margin-bottom: 20px; }}
    summary {{
      font-size: .82rem; color: #888; cursor: pointer;
      user-select: none; padding: 4px 0;
    }}
    .howto {{
      font-size: .82rem; color: #555; margin-top: 10px; line-height: 1.6;
      background: #f9f9f6; border-radius: 6px; padding: 12px 14px;
    }}
    code {{
      background: rgba(0,0,0,.06); padding: 1px 5px; border-radius: 3px;
      font-size: .9em;
    }}
  </style>
</head>
<body>
  <div class="card">
    <p class="step">Step 2 of 2</p>
    <h1>Connect your Substack</h1>
    <p class="sub">Enter your Substack session cookies so the gateway can act on your behalf</p>
    {error}
    <details>
      <summary>How do I find these values?</summary>
      <div class="howto">
        <ol style="padding-left:18px">
          <li>Open <strong>substack.com</strong> and sign in</li>
          <li>Open DevTools → Application → Cookies → <code>https://substack.com</code></li>
          <li>Copy the values for <code>substack.sid</code> and <code>connect.sid</code></li>
        </ol>
      </div>
    </details>
    <form method="post">
      <input type="hidden" name="session_id" value="{session_id}">

      <label for="substack_sid">substack.sid cookie</label>
      <input type="password" id="substack_sid" name="substack_sid" required
             placeholder="s%3A…">
      <p class="hint">Value of the <code>substack.sid</code> cookie</p>

      <label for="connect_sid">connect.sid cookie</label>
      <input type="password" id="connect_sid" name="connect_sid" required
             placeholder="s%3A…">
      <p class="hint">Value of the <code>connect.sid</code> cookie</p>

      <label for="pub_url">Publication URL</label>
      <input type="url" id="pub_url" name="pub_url" required
             placeholder="https://yourname.substack.com"
             style="font-family:inherit">
      <p class="hint">Your Substack publication URL (no trailing slash)</p>

      <button type="submit">Authorize</button>
    </form>
  </div>
</body>
</html>
"""
