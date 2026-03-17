from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from gateway_oss.config import settings
from starlette.responses import Response
from starlette.routing import Route, Router

from gateway_pro.oauth.login import process_login, process_token_form
from gateway_pro.oauth.templates import render_login, render_token_form

oauth_provider = None
if settings.oauth_enabled:
    from gateway_pro.oauth.provider import NeonOAuthProvider

    assert settings.base_url, "BASE_URL must be set when OAuth is enabled"
    oauth_provider = NeonOAuthProvider(
        base_url=f"{settings.base_url}/mcp",
        login_base_url=settings.base_url,
    )

# ── Well-known discovery (RFC 8414 / RFC 9728) ────────────────────────────────

_well_known = Router(
    routes=[
        Route(
            r.path.removeprefix("/.well-known"),
            r.endpoint,
            methods=list(r.methods) if r.methods else None,
        )
        for r in (
            oauth_provider.get_well_known_routes() if oauth_provider is not None else []
        )
    ]
)

# ── Login flow ─────────────────────────────────────────────────────────────────

_login_router = APIRouter(tags=["oauth"])


@_login_router.get("/", response_class=HTMLResponse)
async def login_get(request_id: str = "") -> Response:
    return render_login(request_id)


@_login_router.post("/", response_class=HTMLResponse)
async def login_post(request: Request) -> Response:
    from gateway_oss.config import settings

    return await process_login(request, f"{settings.base_url}/login/token")


@_login_router.get("/token", response_class=HTMLResponse)
async def login_token_get(session_id: str = "") -> Response:
    return render_token_form(session_id)


@_login_router.post("/token", response_class=HTMLResponse)
async def login_token_post(request: Request) -> Response:
    return await process_token_form(request)


_login = FastAPI()
_login.include_router(_login_router)
_login.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="oauth-static",
)

# ── Top-level OAuth app (mounted at "/" in main.py) ───────────────────────────
# Handles /.well-known/* and /login/* so all OAuth concerns live here.

oauth = FastAPI()
oauth.mount("/.well-known", _well_known)
oauth.mount("/login", _login)
