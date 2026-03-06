"""Two-phase login route handlers.

Phase 1 (/login)       — email + password → login session
Phase 2 (/login/token) — Substack cookie values → auth code + redirect
"""

from __future__ import annotations

import html as _html
import secrets
import time
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
from mcp.server.auth.provider import construct_redirect_uri
from sqlalchemy import delete, func, insert, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response

from gateway.oauth.bearer import _encode_bearer, _validate_bearer
from gateway.oauth.db import (
    get_engine,
    t_auth_codes,
    t_auth_requests,
    t_login_sessions,
    t_user_credentials,
    t_users,
)
from gateway.oauth.templates import _LOGIN_HTML, _TOKEN_HTML

_UTC = timezone.utc
_AUTH_CODE_TTL = 300  # seconds
_LOGIN_SESSION_TTL = 600  # seconds


# ------------------------------------------------------------------
# Rendering helpers
# ------------------------------------------------------------------


def render_login(request_id: str, error: str = "") -> Response:
    safe_rid = _html.escape(request_id)
    safe_err = f'<p class="error">{_html.escape(error)}</p>' if error else ""
    return HTMLResponse(_LOGIN_HTML.format(request_id=safe_rid, error=safe_err))


def render_token_form(session_id: str, error: str = "") -> Response:
    safe_sid = _html.escape(session_id)
    safe_err = f'<p class="error">{_html.escape(error)}</p>' if error else ""
    return HTMLResponse(_TOKEN_HTML.format(session_id=safe_sid, error=safe_err))


# ------------------------------------------------------------------
# Phase 1 — email + password
# ------------------------------------------------------------------


async def handle_login(request: Request, base_url: str) -> Response:
    if request.method == "GET":
        return render_login(request.query_params.get("request_id", ""))
    return await _process_login(request, base_url)


async def _process_login(request: Request, base_url: str) -> Response:
    form = await request.form()
    request_id = str(form.get("request_id", "")).strip()
    email = str(form.get("email", "")).strip().lower()
    password = str(form.get("password", ""))

    if not (request_id and email and password):
        return render_login(request_id, "All fields are required.")

    async with get_engine().connect() as conn:
        row = await conn.execute(
            select(t_auth_requests.c.expires_at).where(
                t_auth_requests.c.request_id == request_id
            )
        )
        rec = row.fetchone()

    if rec is None:
        return render_login(request_id, "Session expired. Please try again.")
    expires_at = rec[0]
    if hasattr(expires_at, "tzinfo") and expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=_UTC)
    if datetime.now(_UTC) > expires_at:
        return render_login(request_id, "Session expired. Please try again.")

    async with get_engine().connect() as conn:
        row = await conn.execute(
            select(t_users.c.id, t_users.c.hashed_password).where(
                t_users.c.email == email
            )
        )
        user_rec = row.fetchone()

    if user_rec is None or not bcrypt.checkpw(
        password.encode(), user_rec[1].encode()
    ):
        return render_login(request_id, "Invalid email or password.")

    user_id: int = user_rec[0]
    session_id = str(uuid.uuid4())
    session_expires = datetime.now(_UTC) + timedelta(seconds=_LOGIN_SESSION_TTL)
    async with get_engine().begin() as conn:
        await conn.execute(
            insert(t_login_sessions).values(
                session_id=session_id,
                request_id=request_id,
                user_id=user_id,
                expires_at=session_expires,
            )
        )

    redirect = f"{base_url.rstrip('/')}/login/token?session_id={session_id}"
    return RedirectResponse(url=redirect, status_code=302)


# ------------------------------------------------------------------
# Phase 2 — Substack bearer token
# ------------------------------------------------------------------


async def handle_token_form(request: Request) -> Response:
    if request.method == "GET":
        return render_token_form(request.query_params.get("session_id", ""))
    return await _process_token_form(request)


async def _process_token_form(request: Request) -> Response:
    form = await request.form()
    session_id = str(form.get("session_id", "")).strip()
    substack_sid = str(form.get("substack_sid", "")).strip()
    connect_sid = str(form.get("connect_sid", "")).strip()
    pub_url = str(form.get("pub_url", "")).strip().rstrip("/")

    if not (session_id and substack_sid and connect_sid and pub_url):
        return render_token_form(session_id, "All fields are required.")

    async with get_engine().connect() as conn:
        row = await conn.execute(
            select(
                t_login_sessions.c.request_id,
                t_login_sessions.c.user_id,
                t_login_sessions.c.expires_at,
            ).where(t_login_sessions.c.session_id == session_id)
        )
        sess = row.fetchone()

    if sess is None:
        return render_token_form(session_id, "Session expired. Please start over.")
    request_id, user_id, sess_expires = sess
    if hasattr(sess_expires, "tzinfo") and sess_expires.tzinfo is None:
        sess_expires = sess_expires.replace(tzinfo=_UTC)
    if datetime.now(_UTC) > sess_expires:
        return render_token_form(session_id, "Session expired. Please start over.")

    async with get_engine().connect() as conn:
        row = await conn.execute(
            select(
                t_auth_requests.c.client_id,
                t_auth_requests.c.code_challenge,
                t_auth_requests.c.redirect_uri,
                t_auth_requests.c.redirect_uri_provided_explicitly,
                t_auth_requests.c.scopes,
                t_auth_requests.c.state,
                t_auth_requests.c.resource,
            ).where(t_auth_requests.c.request_id == request_id)
        )
        auth_req = row.fetchone()

    if auth_req is None:
        return render_token_form(session_id, "OAuth session expired. Please start over.")
    cid, code_challenge, redirect_uri, ruri_ex, scopes_str, state, resource = auth_req

    bearer = _encode_bearer(substack_sid, connect_sid)
    try:
        _validate_bearer(bearer)
    except ValueError as exc:
        return render_token_form(session_id, str(exc))

    stmt = pg_insert(t_user_credentials).values(
        user_id=user_id, bearer=bearer, pub_url=pub_url
    )
    async with get_engine().begin() as conn:
        await conn.execute(
            stmt.on_conflict_do_update(
                index_elements=["user_id"],
                set_={
                    "bearer": stmt.excluded.bearer,
                    "pub_url": stmt.excluded.pub_url,
                    "updated_at": func.now(),
                },
            )
        )

    code = secrets.token_urlsafe(32)
    exp = time.time() + _AUTH_CODE_TTL
    async with get_engine().begin() as conn:
        await conn.execute(
            insert(t_auth_codes).values(
                code=code,
                client_id=cid,
                redirect_uri=redirect_uri,
                redirect_uri_provided_explicitly=ruri_ex,
                scopes=scopes_str,
                expires_at=exp,
                code_challenge=code_challenge,
                resource=resource,
                user_id=user_id,
            )
        )
        await conn.execute(
            delete(t_login_sessions).where(
                t_login_sessions.c.session_id == session_id
            )
        )
        await conn.execute(
            delete(t_auth_requests).where(
                t_auth_requests.c.request_id == request_id
            )
        )

    redirect_url = construct_redirect_uri(redirect_uri, code=code, state=state)
    return RedirectResponse(url=redirect_url, status_code=302)
