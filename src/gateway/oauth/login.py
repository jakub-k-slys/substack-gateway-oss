"""Two-phase login handlers.

Phase 1 (process_login)       — email + password → login session
Phase 2 (process_token_form)  — base64-encoded Substack token → auth code + redirect
"""

from __future__ import annotations

import secrets
import time
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
from mcp.server.auth.provider import construct_redirect_uri
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from gateway.oauth.bearer import validate_bearer
from gateway.oauth.db import DBAuthCode, DBLoginSession
from gateway.oauth.repositories import UnitOfWork
from gateway.oauth.templates import render_login, render_token_form

_UTC = timezone.utc
_AUTH_CODE_TTL = 300  # seconds
_LOGIN_SESSION_TTL = 600  # seconds


# ------------------------------------------------------------------
# Phase 1 — email + password
# ------------------------------------------------------------------


async def process_login(request: Request, token_form_url: str) -> Response:
    form = await request.form()
    request_id = str(form.get("request_id", "")).strip()
    email = str(form.get("email", "")).strip().lower()
    password = str(form.get("password", ""))

    if not (request_id and email and password):
        return render_login(request_id, "All fields are required.")

    async with UnitOfWork() as uow:
        auth_req = await uow.auth_requests.get(request_id)
        if auth_req is None:
            return render_login(request_id, "Session expired. Please try again.")
        if datetime.now(_UTC) > auth_req.expires_at:
            return render_login(request_id, "Session expired. Please try again.")

        user = await uow.users.get_by_email(email)
        if user is None or not bcrypt.checkpw(
            password.encode(), user.hashed_password.encode()
        ):
            return render_login(request_id, "Invalid email or password.")

        session_id = str(uuid.uuid4())
        session_expires = datetime.now(_UTC) + timedelta(seconds=_LOGIN_SESSION_TTL)
        await uow.login_sessions.save(
            DBLoginSession(
                session_id=session_id,
                request_id=request_id,
                user_id=user.id,
                expires_at=session_expires,
            )
        )

    redirect = f"{token_form_url}?session_id={session_id}"
    return RedirectResponse(url=redirect, status_code=302)


# ------------------------------------------------------------------
# Phase 2 — Substack bearer token
# ------------------------------------------------------------------


async def process_token_form(request: Request) -> Response:
    form = await request.form()
    session_id = str(form.get("session_id", "")).strip()
    token = str(form.get("token", "")).strip()
    pub_url = str(form.get("pub_url", "")).strip().rstrip("/")

    if not (session_id and token and pub_url):
        return render_token_form(session_id, "All fields are required.")

    try:
        validate_bearer(token)
    except ValueError as exc:
        return render_token_form(session_id, str(exc))

    async with UnitOfWork() as uow:
        login_sess = await uow.login_sessions.get(session_id)
        if login_sess is None:
            return render_token_form(session_id, "Session expired. Please start over.")
        if datetime.now(_UTC) > login_sess.expires_at:
            return render_token_form(session_id, "Session expired. Please start over.")

        auth_req = await uow.auth_requests.get(login_sess.request_id)
        if auth_req is None:
            return render_token_form(
                session_id, "OAuth session expired. Please start over."
            )

        await uow.user_credentials.upsert(login_sess.user_id, token, pub_url)

        code = secrets.token_urlsafe(32)
        exp = time.time() + _AUTH_CODE_TTL
        await uow.auth_codes.save(
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
        await uow.login_sessions.delete(session_id)
        await uow.auth_requests.delete(login_sess.request_id)

    redirect_url = construct_redirect_uri(
        auth_req.redirect_uri, code=code, state=auth_req.state
    )
    return RedirectResponse(url=redirect_url, status_code=302)
