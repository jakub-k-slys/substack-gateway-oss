from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack
from typing import Any

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount, Route

from gateway_oss.api.app import api
from gateway_oss.extensions.runtime import get_runtime
from gateway_oss.mcp.app import mcp


@contextlib.asynccontextmanager
async def _lifespan(app: Any) -> AsyncIterator[None]:
    runtime = get_runtime()
    async with AsyncExitStack() as stack:
        for hook in runtime.lifespan_hooks:
            await stack.enter_async_context(hook(app))
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
    app = Starlette(lifespan=_lifespan, routes=routes)
    app.add_middleware(
        CORSMiddleware,  # type: ignore[arg-type]
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    runtime = get_runtime()
    app.state.gateway_runtime = runtime
    for extension in runtime.extensions:
        extension.register_app(app, runtime.context)
    return app
