from __future__ import annotations

from gateway_core.capabilities import RestCapability

_FEATURES = (
    "api:profiles:get",
    "api:profiles:posts:list",
    "api:profiles:notes:list",
)


def capability() -> RestCapability:
    from gateway_profiles_rest.router import router

    return RestCapability(
        domain="profiles", router=router, mount_prefix="/v1", features=_FEATURES
    )
