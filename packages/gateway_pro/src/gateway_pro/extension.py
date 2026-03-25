from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator, Sequence
from typing import Any

from fastapi import FastAPI
from fastmcp import FastMCP
from gateway_oss.extensions.base import (
    ApplicationInfo,
    GatewayExtension,
    GatewayExtensionContext,
    LifespanHook,
)
from starlette.applications import Starlette
from starlette.routing import Mount

from gateway_pro import __version__ as pro_version


class ProExtension(GatewayExtension):
    name = "gateway_pro"

    def register_api(self, api: FastAPI, context: GatewayExtensionContext) -> None:
        from gateway_pro.api.v1 import router as pro_router

        api.include_router(pro_router, prefix="/v1")

    def register_app(self, app: Starlette, context: GatewayExtensionContext) -> None:
        from gateway_pro.oauth.router import oauth

        app.router.routes.append(Mount("/", app=oauth))

    def register_mcp(self, mcp: FastMCP, context: GatewayExtensionContext) -> None:
        from gateway_pro.mcp.app import register_routes, register_tools

        register_tools(mcp)
        register_routes(mcp)

    def get_lifespan_hooks(
        self, context: GatewayExtensionContext
    ) -> Sequence[LifespanHook]:
        return [self._init_db]

    def get_mcp_auth_provider(self, context: GatewayExtensionContext) -> Any | None:
        from gateway_pro.oauth.router import oauth_provider

        return oauth_provider

    def get_application_info(
        self, context: GatewayExtensionContext
    ) -> ApplicationInfo | None:
        return ApplicationInfo(
            application="substack-gateway",
            tier="pro",
            version=pro_version,
        )

    @contextlib.asynccontextmanager
    async def _init_db(self, app: Any) -> AsyncIterator[None]:
        from gateway_pro.oauth.db import init_db

        await init_db()
        yield


def get_extension() -> GatewayExtension:
    return ProExtension()
