from __future__ import annotations

OSS_FEATURES: tuple[str, ...] = (
    "api:health:live",
    "api:health:ready",
)


def build_oss_features() -> tuple[str, ...]:
    return tuple(sorted(OSS_FEATURES))
