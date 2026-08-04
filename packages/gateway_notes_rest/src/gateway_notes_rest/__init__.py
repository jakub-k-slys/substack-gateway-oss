from __future__ import annotations

from gateway_core.capabilities import RestCapability

_FEATURES = (
    "api:notes:get",
    "api:notes:create",
    "api:notes:delete",
    "api:notes:like",
    "api:notes:unlike",
    "api:notes:reply",
    "api:notes:replies:list",
)


def capability() -> RestCapability:
    from gateway_notes_rest.router import router

    return RestCapability(
        domain="notes", router=router, mount_prefix="/v1", features=_FEATURES
    )
