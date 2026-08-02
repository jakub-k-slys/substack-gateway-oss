from __future__ import annotations

from typing import Any

from gateway_oss.extensions.base import (
    GatewayExtension,
    GatewayExtensionContext,
    LifespanHook,
)

__all__ = [
    "GatewayExtension",
    "GatewayExtensionContext",
    "GatewayRuntime",
    "LifespanHook",
    "get_runtime",
]


def __getattr__(name: str) -> Any:
    # Lazy re-export to avoid a gateway_oss -> shell eager edge: importing
    # gateway_oss.extensions.base must not pull substack_gateway.runtime (which
    # imports gateway_oss.extensions.base back), or the runtime shim would
    # re-enter a partially-initialised module.
    if name in ("GatewayRuntime", "get_runtime"):
        from substack_gateway.runtime import GatewayRuntime, get_runtime

        return {"GatewayRuntime": GatewayRuntime, "get_runtime": get_runtime}[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
