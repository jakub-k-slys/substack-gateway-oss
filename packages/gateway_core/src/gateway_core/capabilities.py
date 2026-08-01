from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import APIRouter
    from fastmcp import FastMCP


@dataclass(frozen=True)
class RestCapability:
    """REST capability descriptor for one domain, published via an entry-point."""

    domain: str
    router: APIRouter
    mount_prefix: str = "/v1"
    features: tuple[str, ...] = ()


@dataclass(frozen=True)
class McpCapability:
    """MCP capability descriptor for one domain, published via an entry-point."""

    domain: str
    register: Callable[[FastMCP], None]
    features: tuple[str, ...] = ()
