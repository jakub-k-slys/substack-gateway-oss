from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, TypeVar

from gateway_oss.config import settings
from gateway_oss.extensions.base import (
    ApplicationInfo,
    GatewayExtension,
    GatewayExtensionContext,
    LifespanHook,
)
from gateway_oss.extensions.loader import load_extensions

T = TypeVar("T")


@dataclass(slots=True)
class GatewayRuntime:
    context: GatewayExtensionContext
    extensions: list[GatewayExtension]
    lifespan_hooks: list[LifespanHook]
    mcp_auth_provider: Any | None
    application_info: ApplicationInfo | None


def _single_provider(label: str, providers: Sequence[T | None]) -> T | None:
    active = [provider for provider in providers if provider is not None]
    if len(active) > 1:
        raise RuntimeError(f"Expected at most one {label}, found {len(active)}")
    return active[0] if active else None


@lru_cache(maxsize=1)
def get_runtime() -> GatewayRuntime:
    context = GatewayExtensionContext(settings=settings)
    extensions = load_extensions()
    lifespan_hooks = [
        hook
        for extension in extensions
        for hook in extension.get_lifespan_hooks(context)
    ]
    mcp_auth_provider = _single_provider(
        "MCP auth provider",
        [extension.get_mcp_auth_provider(context) for extension in extensions],
    )
    application_info = _single_provider(
        "application info provider",
        [extension.get_application_info(context) for extension in extensions],
    )
    return GatewayRuntime(
        context=context,
        extensions=extensions,
        lifespan_hooks=lifespan_hooks,
        mcp_auth_provider=mcp_auth_provider,
        application_info=application_info,
    )
