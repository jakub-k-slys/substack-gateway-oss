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

from gateway_oss.api.app import api
from gateway_oss.application_features import build_oss_features
from gateway_oss.extensions.base import ModuleInfo
from gateway_oss.extensions.runtime import get_runtime
from gateway_oss.mcp.app import mcp
from gateway_oss.versioning import get_package_version

_log = logging.getLogger(__name__)

APPLICATION_NAME = "substack-gateway"


def _oss_module() -> ModuleInfo:
    return ModuleInfo(
        name="gateway-oss",
        version=get_package_version("gateway_oss"),
        features=build_oss_features(),
    )


def _build_modules() -> list[ModuleInfo]:
    runtime = get_runtime()
    modules = [_oss_module(), *runtime.module_infos]
    return [
        ModuleInfo(
            name=module.name,
            version=module.version,
            features=tuple(sorted(set(module.features))),
        )
        for module in modules
    ]


@contextlib.asynccontextmanager
async def _lifespan(app: Any) -> AsyncIterator[None]:
    runtime = get_runtime()
    async with AsyncExitStack() as stack:
        for hook in runtime.lifespan_hooks:
            await stack.enter_async_context(hook(app))
        async with mcp.lifespan(app):
            modules = _build_modules()
            _log.info(
                "Starting %s modules=%s",
                APPLICATION_NAME,
                ",".join(f"{module.name}@{module.version}" for module in modules),
            )
            yield


class _McpTrailingSlash:
    """ASGI app that adds a trailing slash and forwards to the MCP app."""

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        scope = dict(scope, path="/")
        await mcp(scope, receive, send)


async def _root(_: Any) -> JSONResponse:
    return JSONResponse(
        {
            "application": APPLICATION_NAME,
            "modules": [
                {
                    "name": module.name,
                    "version": module.version,
                    "features": list(module.features),
                }
                for module in _build_modules()
            ],
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
