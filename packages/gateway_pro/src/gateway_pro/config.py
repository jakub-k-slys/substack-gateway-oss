from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SUBSTACK_GATEWAY_PRO_")

    following_feed_profile_cache_ttl_sec: int = Field(
        default=14400,
        ge=1,
        validation_alias=AliasChoices(
            "SUBSTACK_GATEWAY_PRO_FOLLOWING_FEED_PROFILE_CACHE_TTL_SEC",
            "SUBSTACK_GATEWAY_FOLLOWING_FEED_PROFILE_CACHE_TTL_SEC",
        ),
    )
    base_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "SUBSTACK_GATEWAY_PRO_BASE_URL",
            "SUBSTACK_GATEWAY_BASE_URL",
        ),
    )
    database_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "SUBSTACK_GATEWAY_PRO_DATABASE_URL",
            "SUBSTACK_GATEWAY_DATABASE_URL",
        ),
    )
    jwt_secret: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "SUBSTACK_GATEWAY_PRO_JWT_SECRET",
            "SUBSTACK_GATEWAY_JWT_SECRET",
        ),
    )

    @property
    def oauth_enabled(self) -> bool:
        return bool(self.base_url and self.database_url and self.jwt_secret)


pro_settings = ProSettings()
