"""Two-phase login route handlers.

Phase 1 (/login)       — email + password → login session
Phase 2 (/login/token) — Substack cookie values → auth code + redirect
"""

from __future__ import annotations

import secrets
import time
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
from mcp.server.auth.provider import construct_redirect_uri
from sqlalchemy import delete, func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from gateway.oauth.bearer import _encode_bearer, _validate_bearer
from gateway.oauth.db import (
    DBAuthCode,
    DBAuthRequest,
    DBLoginSession,
    DBUser,
    DBUserCredential,
    get_session,
)
from gateway.oauth.templates import render_login, render_token_form

_UTC = timezone.utc
_AUTH_CODE_TTL = 300  # seconds
_LOGIN_SESSION_TTL = 600  # seconds


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

    async with get_session() as db:
        auth_req = await db.get(DBAuthRequest, request_id)

    if auth_req is None:
        return render_login(request_id, "Session expired. Please try again.")
    if datetime.now(_UTC) > auth_req.expires_at:
        return render_login(request_id, "Session expired. Please try again.")

    async with get_session() as db:
        result = await db.execute(select(DBUser).where(DBUser.email == email))
        user = result.scalar_one_or_none()

    if user is None or not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        return render_login(request_id, "Invalid email or password.")

    session_id = str(uuid.uuid4())
    session_expires = datetime.now(_UTC) + timedelta(seconds=_LOGIN_SESSION_TTL)
    async with get_session() as db:
        db.add(
            DBLoginSession(
                session_id=session_id,
                request_id=request_id,
                user_id=user.id,
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

    async with get_session() as db:
        login_sess = await db.get(DBLoginSession, session_id)

    if login_sess is None:
        return render_token_form(session_id, "Session expired. Please start over.")
    if datetime.now(_UTC) > login_sess.expires_at:
        return render_token_form(session_id, "Session expired. Please start over.")

    async with get_session() as db:
        auth_req = await db.get(DBAuthRequest, login_sess.request_id)

    if auth_req is None:
        return render_token_form(session_id, "OAuth session expired. Please start over.")

    bearer = _encode_bearer(substack_sid, connect_sid)
    try:
        _validate_bearer(bearer)
    except ValueError as exc:
        return render_token_form(session_id, str(exc))

    # Upsert Substack credentials
    stmt = pg_insert(DBUserCredential).values(
        user_id=login_sess.user_id, bearer=bearer, pub_url=pub_url
    )
    async with get_session() as db:
        await db.execute(
            stmt.on_conflict_do_update(
                index_elements=["user_id"],
                set_={
                    "bearer": stmt.excluded.bearer,
                    "pub_url": stmt.excluded.pub_url,
                    "updated_at": func.now(),
                },
            )
        )

    # Issue auth code and clean up transient rows atomically
    code = secrets.token_urlsafe(32)
    exp = time.time() + _AUTH_CODE_TTL
    async with get_session() as db:
        db.add(
            DBAuthCode(
                code=code,
                client_id=auth_req.client_id,
                redirect_uri=auth_req.redirect_uri,
                redirect_uri_provided_explicitly=auth_req.redirect_uri_provided_explicitly,
                scopes=auth_req.scopes,
                expires_at=exp,
                code_challenge=auth_req.code_challenge,
                resource=auth_req.resource,
                user_id=login_sess.user_id,
            )
        )
        await db.execute(
            delete(DBLoginSession).where(DBLoginSession.session_id == session_id)
        )
        await db.execute(
            delete(DBAuthRequest).where(
                DBAuthRequest.request_id == login_sess.request_id
            )
        )

    redirect_url = construct_redirect_uri(
        auth_req.redirect_uri, code=code, state=auth_req.state
    )
    return RedirectResponse(url=redirect_url, status_code=302)
