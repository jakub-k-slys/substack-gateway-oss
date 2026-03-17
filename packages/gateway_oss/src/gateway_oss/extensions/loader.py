from __future__ import annotations

import importlib
import importlib.metadata
import os
from typing import Any

from gateway_oss.extensions.base import GatewayExtension

ENTRYPOINT_GROUP = "substack_gateway_oss.extensions"
ENV_VAR = "GATEWAY_EXTENSION_MODULES"


def _coerce_extension(candidate: Any) -> GatewayExtension:
    extension = candidate() if callable(candidate) else candidate
    return extension


def _load_from_entrypoints() -> list[GatewayExtension]:
    extensions: list[GatewayExtension] = []
    for entrypoint in importlib.metadata.entry_points(group=ENTRYPOINT_GROUP):
        extensions.append(_coerce_extension(entrypoint.load()))
    return extensions


def _load_from_env() -> list[GatewayExtension]:
    value = os.getenv(ENV_VAR, "").strip()
    if not value:
        return []

    extensions: list[GatewayExtension] = []
    for item in value.split(","):
        module_name, _, attr = item.strip().partition(":")
        module = importlib.import_module(module_name)
        candidate: Any = module if not attr else getattr(module, attr)
        extensions.append(_coerce_extension(candidate))
    return extensions


def load_extensions() -> list[GatewayExtension]:
    by_name: dict[str, GatewayExtension] = {}
    for extension in [*_load_from_entrypoints(), *_load_from_env()]:
        by_name[extension.name] = extension
    return list(by_name.values())
