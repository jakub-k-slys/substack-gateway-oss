from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response

from gateway.config import settings
from gateway.oauth.login import process_login, process_token_form
from gateway.oauth.templates import render_login, render_token_form

oauth_provider = None
if settings.oauth_enabled:
    from gateway.oauth.provider import NeonOAuthProvider

    assert settings.base_url, "BASE_URL must be set when OAuth is enabled"
    oauth_provider = NeonOAuthProvider(
        base_url=f"{settings.base_url}/mcp",
        login_base_url=settings.base_url,
    )

well_known_routes = (
    oauth_provider.get_well_known_routes() if oauth_provider is not None else []
)

_router = APIRouter(tags=["oauth"])


# Routes at "/" and "/token" because this app is mounted at "/login" in main.py,
# so Starlette strips the "/login" prefix before forwarding to this FastAPI app.


@_router.get("/", response_class=HTMLResponse)
async def login_get(request_id: str = "") -> Response:
    return render_login(request_id)


@_router.post("/", response_class=HTMLResponse)
async def login_post(request: Request) -> Response:
    from gateway.config import settings

    return await process_login(request, f"{settings.base_url}/login/token")


@_router.get("/token", response_class=HTMLResponse)
async def login_token_get(session_id: str = "") -> Response:
    return render_token_form(session_id)


@_router.post("/token", response_class=HTMLResponse)
async def login_token_post(request: Request) -> Response:
    return await process_token_form(request)


oauth = FastAPI()
oauth.include_router(_router)
oauth.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="oauth-static",
)
