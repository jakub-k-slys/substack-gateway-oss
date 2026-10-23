from __future__ import annotations

from collections.abc import Callable

import httpx

TransportFactory = Callable[[httpx.Limits], httpx.AsyncBaseTransport]
"""Builds the transport an ``httpx.AsyncClient`` sends its requests through.

The factory receives the connection limits the gateway would apply and returns
the transport to use, so an extension can wrap or replace the default one.
"""


def default_transport_factory(limits: httpx.Limits) -> httpx.AsyncBaseTransport:
    """Build the stock httpx transport with the gateway's connection limits."""
    return httpx.AsyncHTTPTransport(limits=limits)


_factory: TransportFactory = default_transport_factory


def set_transport_factory(factory: TransportFactory | None) -> None:
    """Install the process-wide transport factory. Pass ``None`` for the default."""
    global _factory
    _factory = default_transport_factory if factory is None else factory


def get_transport_factory() -> TransportFactory:
    """Return the installed transport factory (the default when none is set)."""
    return _factory
