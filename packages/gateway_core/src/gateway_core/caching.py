from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


@runtime_checkable
class ValueCache(Protocol):
    """Caches the result of an async call under a caller-supplied key."""

    async def get_or_call(self, key: str, factory: Callable[[], Awaitable[T]]) -> T:
        """Return the value cached for ``key``, or await ``factory`` and store it.

        Implementations that actually cache MUST collapse concurrent calls for
        the same key onto a single ``factory`` await, so that a cold key under
        load produces one upstream request rather than one per caller.

        There is deliberately no TTL parameter. How long an answer lives is the
        cache's own policy; the caller names only the key and the work.
        """


class NullValueCache:
    """The default: retains nothing, so every call reaches ``factory``."""

    async def get_or_call(self, key: str, factory: Callable[[], Awaitable[T]]) -> T:
        return await factory()


_value_cache: ValueCache = NullValueCache()


def set_value_cache(cache: ValueCache | None) -> None:
    """Install the process-wide value cache. ``None`` restores the null cache."""
    global _value_cache
    _value_cache = cache if cache is not None else NullValueCache()


def get_value_cache() -> ValueCache:
    """Return the installed value cache. Never ``None`` — the null cache is the default."""
    return _value_cache
