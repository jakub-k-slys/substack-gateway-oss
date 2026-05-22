from __future__ import annotations

OSS_FEATURES: tuple[str, ...] = (
    "api:comments:get",
    "api:health:live",
    "api:health:ready",
    "api:me:following:list",
    "api:me:get",
    "api:me:notes:list",
    "api:me:posts:list",
    "api:notes:create",
    "api:notes:delete",
    "api:notes:get",
    "api:posts:comments:list",
    "api:posts:get",
    "api:profiles:get",
    "api:profiles:notes:list",
    "api:profiles:posts:list",
    "mcp:me:following:list",
    "mcp:me:get",
    "mcp:me:notes:list",
    "mcp:me:posts:list",
    "mcp:notes:create",
    "mcp:notes:delete",
    "mcp:notes:get",
    "mcp:posts:comments:list",
    "mcp:posts:get",
    "mcp:profiles:get",
    "mcp:profiles:notes:list",
    "mcp:profiles:posts:list",
)


def build_oss_features() -> tuple[str, ...]:
    return tuple(sorted(OSS_FEATURES))
