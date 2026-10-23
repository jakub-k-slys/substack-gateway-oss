from __future__ import annotations

from collections.abc import Callable

import httpx

TransportFactory = Callable[[httpx.Limits], httpx.AsyncBaseTransport]
"""Builds the transport an ``httpx.AsyncClient`` sends its requests through.

The factory receives the connection limits the gateway would apply and returns
the transport to use, so an extension can wrap or replace the default one.

Ownership: the factory is called once per client, that is, once for each
``async with`` of a Substack client. It must return a NEW transport on every
call, and the client closes that transport when it exits. State that outlives
a single client, such as connection pools or rate limiters, must therefore
live outside the returned transport, and the transport's ``aclose()`` must not
tear it down.

An installed transport takes over connection handling, including proxies,
because httpx disables environment proxies when a transport is supplied.
"""


def default_transport_factory(limits: httpx.Limits) -> httpx.AsyncBaseTransport:
    """Build the stock httpx transport with the gateway's connection limits."""
    return httpx.AsyncHTTPTransport(limits=limits)


_factory: TransportFactory = default_transport_factory


def set_transport_factory(factory: TransportFactory | None) -> None:
    """Install the process-wide transport factory. Pass ``None`` for the default.

    The factory is called once per client and must return a new transport each
    time; the client closes it on exit. Keep long-lived shared state (pools,
    rate limiters) outside the transport, whose ``aclose()`` must not tear it
    down.

    An installed transport takes over connection handling, including proxies,
    because httpx disables environment proxies when a transport is supplied.
    """
    global _factory
    _factory = default_transport_factory if factory is None else factory


def get_transport_factory() -> TransportFactory:
    """Return the installed transport factory (the default when none is set)."""
    return _factory
