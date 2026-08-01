from __future__ import annotations

OSS_FEATURES: tuple[str, ...] = (
    "api:health:live",
    "api:health:ready",
    "api:me:get",
    "api:me:notes:list",
    "api:me:posts:list",
    "api:profiles:get",
    "api:profiles:notes:list",
    "api:profiles:posts:list",
    "mcp:me:get",
    "mcp:me:notes:list",
    "mcp:me:posts:list",
    "mcp:profiles:get",
    "mcp:profiles:notes:list",
    "mcp:profiles:posts:list",
)


def build_oss_features() -> tuple[str, ...]:
    return tuple(sorted(OSS_FEATURES))
