from __future__ import annotations

from gateway_core.capabilities import RestCapability

_FEATURES = ("api:posts:get",)


def capability() -> RestCapability:
    from gateway_posts_rest.router import router

    return RestCapability(
        domain="posts", router=router, mount_prefix="/v1", features=_FEATURES
    )
