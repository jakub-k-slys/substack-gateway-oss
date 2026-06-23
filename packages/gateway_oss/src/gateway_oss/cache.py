from __future__ import annotations

import logging
from urllib.parse import urlparse

import aiocache

from gateway_oss.config import settings

_log = logging.getLogger(__name__)

DEFAULT_ALIAS = "default"


def configure_default_cache() -> None:
    """Configure the shared aiocache ``"default"`` alias from settings.

    A single setting (``SUBSTACK_GATEWAY_REDIS_URL``) selects the backend for the
    whole application: Redis/Dragonfly when set, in-process memory otherwise. The
    same alias is shared by every ``@cached``/``@cached_stampede(alias="default")``
    decorator across OSS and any loaded extensions.

    This MUST run before any module that decorates functions with that alias is
    imported, because aiocache binds the concrete cache instance at decoration
    time (not at call time). Importing the ``gateway_oss`` package triggers it (see
    ``gateway_oss/__init__.py``), which guarantees the correct backend is in place
    before any OSS or extension service module is imported. It is idempotent and
    cheap, so it is safe to call again (e.g. from tests).
    """
    if settings.redis_url:
        parsed = urlparse(settings.redis_url)
        aiocache.caches.set_config(
            {
                DEFAULT_ALIAS: {
                    "cache": "aiocache.RedisCache",
                    "endpoint": parsed.hostname or "localhost",
                    "port": parsed.port or 6379,
                    "password": parsed.password,
                    "serializer": {"class": "aiocache.serializers.PickleSerializer"},
                }
            }
        )
        _log.info("Cache: Redis at %s:%s", parsed.hostname, parsed.port)
    else:
        aiocache.caches.set_config(
            {
                DEFAULT_ALIAS: {
                    "cache": "aiocache.SimpleMemoryCache",
                    "serializer": {"class": "aiocache.serializers.NullSerializer"},
                }
            }
        )
        _log.info(
            "Cache: in-process SimpleMemoryCache (SUBSTACK_GATEWAY_REDIS_URL not set)"
        )
