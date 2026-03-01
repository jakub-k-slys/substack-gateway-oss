from __future__ import annotations

from starlette.applications import Starlette
from starlette.routing import Mount

from gateway import api, mcp

app = Starlette(
    routes=[
        Mount("/mcp", app=mcp.http_app()),
        Mount("/api", app=api),
    ]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True, loop="uvloop")
