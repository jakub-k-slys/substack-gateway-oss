from __future__ import annotations

from gateway_core.capabilities import RestCapability

_FEATURES = ("api:comments:get", "api:posts:comments:list")


def capability() -> RestCapability:
    from gateway_comments_rest.router import router

    return RestCapability(
        domain="comments", router=router, mount_prefix="/v1", features=_FEATURES
    )
