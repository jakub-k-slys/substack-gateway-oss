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

PRO_FEATURES: tuple[str, ...] = (
    "api:drafts:create",
    "api:drafts:delete",
    "api:drafts:get",
    "api:drafts:list",
    "api:drafts:update",
    "api:feeds:batch:atom",
    "api:feeds:batch:create",
    "api:feeds:batch:get",
    "api:feeds:batch:list",
    "api:feeds:batch:upsert",
    "api:me:following:feed",
    "api:notes:like",
    "api:notes:unlike",
    "api:posts:like",
    "api:posts:restack",
    "api:posts:unlike",
    "api:profiles:feed",
    "mcp:drafts:create",
    "mcp:drafts:delete",
    "mcp:drafts:get",
    "mcp:drafts:list",
    "mcp:drafts:update",
    "mcp:feeds:batch:create",
    "mcp:feeds:batch:get",
    "mcp:feeds:batch:list",
    "mcp:feeds:batch:upsert",
    "mcp:notes:like",
    "mcp:notes:unlike",
    "mcp:posts:like",
    "mcp:posts:restack",
    "mcp:posts:unlike",
)

PRO_OAUTH_FEATURES: tuple[str, ...] = (
    "api:users:create",
    "api:users:delete",
)


def build_oss_features() -> tuple[str, ...]:
    return tuple(sorted(OSS_FEATURES))


def build_pro_features(*, oauth_enabled: bool) -> tuple[str, ...]:
    features = set(OSS_FEATURES)
    features.update(PRO_FEATURES)
    if oauth_enabled:
        features.update(PRO_OAUTH_FEATURES)
    return tuple(sorted(features))
