from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import APIRouter
    from fastmcp import FastMCP


@dataclass(frozen=True)
class RestCapability:
    """Deskryptor komórki REST jednej domeny, publikowany przez entry-point."""

    domain: str
    router: APIRouter
    mount_prefix: str = "/v1"
    features: tuple[str, ...] = ()


@dataclass(frozen=True)
class McpCapability:
    """Deskryptor komórki MCP jednej domeny, publikowany przez entry-point."""

    domain: str
    register: Callable[[FastMCP], None]
    features: tuple[str, ...] = ()
