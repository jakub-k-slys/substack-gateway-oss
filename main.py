from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from typing import Any

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount

from gateway import api, mcp
from gateway.oauth.db import init_db
from gateway.oauth.router import oauth, well_known


@contextlib.asynccontextmanager
async def _lifespan(app: Any) -> AsyncIterator[None]:
    await init_db()
    async with mcp.lifespan(app):
        yield


app = Starlette(
    lifespan=_lifespan,
    routes=[
        Mount("/.well-known", app=well_known),
        Mount("/login", app=oauth),
        Mount("/mcp", app=mcp),
        Mount("/api", app=api),
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
