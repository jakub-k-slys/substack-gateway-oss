from __future__ import annotations

import contextlib
import logging
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack
from typing import Any, cast

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from gateway_oss import __app_version__
from gateway_oss.api.app import api
from gateway_oss.application_features import build_oss_features
from gateway_oss.extensions.base import ApplicationInfo
from gateway_oss.extensions.runtime import get_runtime
from gateway_oss.mcp.app import mcp

_log = logging.getLogger(__name__)


def _get_application_info() -> ApplicationInfo:
    runtime = get_runtime()
    info = runtime.application_info or ApplicationInfo(
        application="substack-gateway",
        tier="oss",
        version=__app_version__,
        features=build_oss_features(),
    )
    return ApplicationInfo(
        application=info.application,
        tier=info.tier,
        version=info.version,
        features=tuple(sorted(set(info.features))),
    )


@contextlib.asynccontextmanager
async def _lifespan(app: Any) -> AsyncIterator[None]:
    runtime = get_runtime()
    async with AsyncExitStack() as stack:
        for hook in runtime.lifespan_hooks:
            await stack.enter_async_context(hook(app))
        async with mcp.lifespan(app):
            info = _get_application_info()
            _log.info(
                "Starting %s tier=%s version=%s features=%s",
                info.application,
                info.tier,
                info.version,
                ",".join(info.features),
            )
            yield


class _McpTrailingSlash:
    """ASGI app that adds a trailing slash and forwards to the MCP app."""

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        scope = dict(scope, path="/")
        await mcp(scope, receive, send)


async def _root(_: Any) -> JSONResponse:
    info = _get_application_info()
    return JSONResponse(
        {
            "application": info.application,
            "tier": info.tier,
            "version": info.version,
            "features": list(info.features),
        }
    )


def create_app() -> Starlette:
    routes: list[Any] = [
        Route("/", _root),
        Route("/mcp", _McpTrailingSlash(), methods=["GET", "POST", "DELETE"]),
        Mount("/mcp", app=mcp),
        Mount("/api", app=api),
    ]
    app = Starlette(lifespan=_lifespan, routes=routes)
    app.add_middleware(
        cast(Any, CORSMiddleware),
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    runtime = get_runtime()
    app.state.gateway_runtime = runtime
    for extension in runtime.extensions:
        extension.register_app(app, runtime.context)
    return app
