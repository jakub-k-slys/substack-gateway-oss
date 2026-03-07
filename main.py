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


async def _mcp_no_trailing_slash(scope: Any, receive: Any, send: Any) -> None:
    """Forward /mcp (no trailing slash) to the MCP app as /mcp/."""
    scope = dict(scope, path=scope["path"] + "/")
    await mcp(scope, receive, send)


app = Starlette(
    lifespan=_lifespan,
    routes=[
        Route(
            "/mcp", endpoint=_mcp_no_trailing_slash, methods=["GET", "POST", "DELETE"]
        ),
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
