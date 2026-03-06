from __future__ import annotations

from typing import Literal
from urllib.parse import urlparse

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SUBSTACK_GATEWAY_")

    substack_base_url: str = "https://substack.com"
    substack_timeout: float = Field(default=10.0, gt=0, le=60)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    gateway_key: str = "WW91IHNoYWxsIG5vdCBwYXNzCg=="

    # OAuth 2.1 / Neon DB settings (all required for OAuth to be active)
    base_url: str | None = None
    database_url: str | None = None
    jwt_secret: str | None = None

    @property
    def oauth_enabled(self) -> bool:
        return bool(self.base_url and self.database_url and self.jwt_secret)

    @field_validator("substack_base_url")
    @classmethod
    def _validate_base_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError(
                f"substack_base_url must be a valid HTTP or HTTPS URL, got {v!r}"
            )
        return v


settings = Settings()
