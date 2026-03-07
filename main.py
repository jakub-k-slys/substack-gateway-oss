from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from typing import Any

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount, Route

from gateway import api, mcp
from gateway.oauth.db import init_db
from gateway.oauth.router import oauth


@contextlib.asynccontextmanager
async def _lifespan(app: Any) -> AsyncIterator[None]:
    await init_db()
    async with mcp.lifespan(app):
        yield


class _McpTrailingSlash:
    """ASGI app that adds a trailing slash and forwards to the MCP app.

    Used as a Route app so /mcp is handled the same as /mcp/.
    Starlette Route(endpoint=) wraps callables as HTTP endpoints (passing
    Request), so we need a raw ASGI app instead.
    """

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        scope = dict(scope, path="/")
        await mcp(scope, receive, send)


app = Starlette(
    lifespan=_lifespan,
    routes=[
        Route("/mcp", _McpTrailingSlash(), methods=["GET", "POST", "DELETE"]),
        Mount("/mcp", app=mcp),
        Mount("/api", app=api),
        Mount("/", app=oauth),
    ],
)

app.add_middleware(
    CORSMiddleware,  # type: ignore[arg-type]
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True, loop="uvloop")
