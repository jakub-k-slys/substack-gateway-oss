from __future__ import annotations

from gateway_core.capabilities import RestCapability

_FEATURES = (
    "api:comments:get",
    "api:comments:create",
    "api:comments:delete",
    "api:comments:like",
    "api:comments:unlike",
    "api:comments:reply",
    "api:comments:replies:list",
    "api:posts:comments:list",
)


def capability() -> RestCapability:
    from gateway_comments_rest.router import router

    return RestCapability(
        domain="comments", router=router, mount_prefix="/v1", features=_FEATURES
    )
