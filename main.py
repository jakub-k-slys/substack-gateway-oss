from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from typing import Any

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount

from gateway import api, mcp
from gateway.mcp.app import oauth_provider
from gateway.oauth.db import init_db


@contextlib.asynccontextmanager
async def _lifespan(app: Any) -> AsyncIterator[None]:
    await init_db()
    async with mcp.lifespan(app):
        yield


# Well-known OAuth discovery routes must be accessible at the root level.
# The MCP app is mounted at /mcp, so without this the /.well-known/* paths
# would incorrectly resolve under /mcp/.well-known/*.
_well_known = (
    oauth_provider.get_well_known_routes() if oauth_provider is not None else []
)

app = Starlette(
    lifespan=_lifespan,
    routes=[
        *_well_known,
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
