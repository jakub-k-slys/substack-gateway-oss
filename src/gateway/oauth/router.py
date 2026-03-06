from __future__ import annotations

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.responses import Response

from gateway.mcp.app import oauth_provider
from gateway.oauth.login import process_login, process_token_form
from gateway.oauth.templates import render_login, render_token_form

well_known_routes = oauth_provider.get_well_known_routes() if oauth_provider is not None else []

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


login_app = FastAPI()
login_app.include_router(_router)
