from __future__ import annotations

from gateway_core.capabilities import RestCapability

_FEATURES = (
    "api:stats:subscribers",
    "api:stats:traffic:30d-views",
    "api:posts:stats:engagement",
    "api:posts:stats:traffic",
    "api:posts:stats:recipients",
    "api:posts:stats:growth",
    "api:posts:stats:discussion",
)


def capability() -> RestCapability:
    from gateway_stats_rest.router import router

    return RestCapability(
        domain="stats", router=router, mount_prefix="/v1", features=_FEATURES
    )
