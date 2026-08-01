from __future__ import annotations

from gateway_core.capabilities import RestCapability

_FEATURES = ("api:me:following:list",)


def capability() -> RestCapability:
    from gateway_following_rest.router import router

    return RestCapability(
        domain="following", router=router, mount_prefix="/v1", features=_FEATURES
    )
