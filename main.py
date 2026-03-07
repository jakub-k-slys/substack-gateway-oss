from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


app = FastAPI(lifespan=_lifespan, docs_url=None, openapi_url=None)
app.add_route("/mcp", _mcp_no_trailing_slash, methods=["GET", "POST", "DELETE"])
app.mount("/mcp", mcp)
app.mount("/api", api)
app.mount("/", oauth)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True, loop="uvloop")
