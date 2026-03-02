from __future__ import annotations

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount

from gateway import api, mcp

mcp_app = mcp.http_app(transport="streamable-http", path="/", stateless_http=True)

app = Starlette(
    lifespan=mcp_app.lifespan,
    routes=[
        Mount("/mcp", app=mcp_app),
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
