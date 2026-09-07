from __future__ import annotations

from gateway_core.capabilities import RestCapability

_FEATURES = (
    "api:drafts:list",
    "api:drafts:get",
    "api:drafts:create",
    "api:drafts:update",
    "api:drafts:delete",
    "api:drafts:schedule",
    "api:drafts:unschedule",
    "api:drafts:prepublish",
    "api:drafts:ai-detection",
    "api:images:create",
)


def capability() -> RestCapability:
    from gateway_drafts_rest.router import router

    return RestCapability(
        domain="drafts", router=router, mount_prefix="/v1", features=_FEATURES
    )
