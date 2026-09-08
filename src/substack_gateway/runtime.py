from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, TypeVar

from gateway_core.credentials import CredentialResolver, set_credential_resolver
from gateway_oss.config import settings
from gateway_oss.extensions.base import (
    GatewayExtension,
    GatewayExtensionContext,
    LifespanHook,
    ModuleInfo,
)
from substack_gateway.ext_loader import load_extensions

T = TypeVar("T")


@dataclass(slots=True)
class GatewayRuntime:
    context: GatewayExtensionContext
    extensions: list[GatewayExtension]
    lifespan_hooks: list[LifespanHook]
    mcp_auth_provider: Any | None
    credential_resolver: CredentialResolver | None
    module_infos: list[ModuleInfo]


def _single_provider(label: str, providers: Sequence[T | None]) -> T | None:
    active = [provider for provider in providers if provider is not None]
    if len(active) > 1:
        raise RuntimeError(f"Expected at most one {label}, found {len(active)}")
    return active[0] if active else None


def _call_optional_hook(
    extension: GatewayExtension, method_name: str, context: GatewayExtensionContext
) -> Any | None:
    """Call an optional protocol method, tolerating extensions that don't define it.

    `ext_loader.load_extensions` never checks a loaded extension against the
    `GatewayExtension` protocol, so a duck-typed extension that doesn't subclass it
    may lack methods the protocol declares with a default. Fall back to `None`
    rather than raising `AttributeError` for those.
    """
    method = getattr(extension, method_name, None)
    if method is None:
        return None
    return method(context)


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
        [
            _call_optional_hook(extension, "get_mcp_auth_provider", context)
            for extension in extensions
        ],
    )
    credential_resolver = _single_provider(
        "credential resolver",
        [
            _call_optional_hook(extension, "get_credential_resolver", context)
            for extension in extensions
        ],
    )
    set_credential_resolver(credential_resolver)
    module_infos = [
        info
        for extension in extensions
        if (info := extension.get_module_info(context)) is not None
    ]
    return GatewayRuntime(
        context=context,
        extensions=extensions,
        lifespan_hooks=lifespan_hooks,
        mcp_auth_provider=mcp_auth_provider,
        credential_resolver=credential_resolver,
        module_infos=module_infos,
    )
