from __future__ import annotations

from gateway_core.cache import configure_default_cache

configure_default_cache()

import contextlib  # noqa: E402
import logging  # noqa: E402
from collections.abc import AsyncIterator  # noqa: E402
from contextlib import AsyncExitStack  # noqa: E402
from typing import Any, cast  # noqa: E402

from starlette.applications import Starlette  # noqa: E402
from starlette.middleware.cors import CORSMiddleware  # noqa: E402
from starlette.responses import JSONResponse  # noqa: E402
from starlette.routing import Mount, Route  # noqa: E402

from gateway_oss.application_features import build_oss_features  # noqa: E402
from gateway_oss.extensions.base import ModuleInfo  # noqa: E402
from gateway_oss.versioning import get_package_version  # noqa: E402
from substack_gateway.api_app import api  # noqa: E402
from substack_gateway.mcp_app import mcp  # noqa: E402
from substack_gateway.runtime import get_runtime  # noqa: E402

_log = logging.getLogger(__name__)

APPLICATION_NAME = "substack-gateway"


def _oss_module() -> ModuleInfo:
    from substack_gateway.registry import load_mcp_capabilities, load_rest_capabilities

    registry_features: tuple[str, ...] = tuple(
        f
        for cap in (*load_rest_capabilities(), *load_mcp_capabilities())
        for f in cap.features
    )
    return ModuleInfo(
        name="gateway-oss",
        version=get_package_version("gateway_oss"),
        features=tuple(sorted({*build_oss_features(), *registry_features})),
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
