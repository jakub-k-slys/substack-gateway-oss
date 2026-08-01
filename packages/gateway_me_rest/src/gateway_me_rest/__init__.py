from __future__ import annotations

from gateway_core.capabilities import RestCapability

_FEATURES = (
    "api:me:get",
    "api:me:notes:list",
    "api:me:posts:list",
)


def capability() -> RestCapability:
    from gateway_me_rest.router import router

    return RestCapability(
        domain="me", router=router, mount_prefix="/v1", features=_FEATURES
    )
