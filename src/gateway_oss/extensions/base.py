from __future__ import annotations

from collections.abc import Callable, Sequence
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from fastapi import FastAPI
from fastmcp import FastMCP
from starlette.applications import Starlette

from gateway_oss.config import Settings

LifespanHook = Callable[[Any], AbstractAsyncContextManager[None, bool | None]]


class CredentialProvider(Protocol):
    async def get_bearer_for_user(self, user_id: int) -> tuple[str, str] | None:
        """Return (bearer_b64, publication_url) or None."""


@dataclass(slots=True)
class GatewayExtensionContext:
    settings: Settings


@dataclass(slots=True, frozen=True)
class ApplicationInfo:
    application: str
    tier: str
    version: str


@runtime_checkable
class GatewayExtension(Protocol):
    name: str

    def register_api(self, api: FastAPI, context: GatewayExtensionContext) -> None:
        """Register additional API routes."""

    def register_app(self, app: Starlette, context: GatewayExtensionContext) -> None:
        """Register Starlette-level routes and middleware."""

    def register_mcp(self, mcp: FastMCP, context: GatewayExtensionContext) -> None:
        """Register MCP tools and custom routes."""

    def get_lifespan_hooks(
        self, context: GatewayExtensionContext
    ) -> Sequence[LifespanHook]:
        """Return lifespan hooks that should be entered when the app starts."""

    def get_credential_provider(
        self, context: GatewayExtensionContext
    ) -> CredentialProvider | None:
        """Return a credential provider for OAuth-backed requests."""

    def get_mcp_auth_provider(self, context: GatewayExtensionContext) -> Any | None:
        """Return an MCP auth provider, if the extension exposes one."""

    def get_application_info(
        self, context: GatewayExtensionContext
    ) -> ApplicationInfo | None:
        """Return application metadata for the root endpoint, if overridden."""
