from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from typing import Any

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount, Route

from gateway.api.app import api
from gateway.mcp.app import mcp


def _load_oauth_app():
    try:
        from gateway_pro.oauth.db import init_db
        from gateway_pro.oauth.router import oauth
    except ImportError:
        return None, None
    return init_db, oauth


@contextlib.asynccontextmanager
async def _lifespan(app: Any) -> AsyncIterator[None]:
    init_db, _oauth = _load_oauth_app()
    if init_db is not None:
        await init_db()
    async with mcp.lifespan(app):
        yield


class _McpTrailingSlash:
    """ASGI app that adds a trailing slash and forwards to the MCP app."""

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        scope = dict(scope, path="/")
        await mcp(scope, receive, send)


def create_app() -> Starlette:
    routes: list[Any] = [
        Route("/mcp", _McpTrailingSlash(), methods=["GET", "POST", "DELETE"]),
        Mount("/mcp", app=mcp),
        Mount("/api", app=api),
    ]
    _init_db, oauth = _load_oauth_app()
    if oauth is not None:
        routes.append(Mount("/", app=oauth))

    app = Starlette(lifespan=_lifespan, routes=routes)
    app.add_middleware(
        CORSMiddleware,  # type: ignore[arg-type]
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
