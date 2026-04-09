from __future__ import annotations

from typing import Literal
from urllib.parse import urlparse

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SUBSTACK_GATEWAY_")

    substack_base_url: str = "https://substack.com"
    substack_timeout_sec: float = Field(default=120.0, gt=0)
    substack_connect_timeout_sec: float = Field(default=120.0, gt=0)
    substack_requests_per_second: float = Field(default=3.0, gt=0)
    substack_retry_attempts: int = Field(default=10, ge=1)
    substack_retry_min_wait_sec: float = Field(default=10.0, gt=0)
    substack_retry_max_wait_sec: float = Field(default=60.0, gt=0)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    admin_token: str = "WW91IHNoYWxsIG5vdCBwYXNzLiBZb3Ugc2hhbGwgbm90IHBhc3MsIHlvdSBzaGFsbCBub3QgcGFzcyEK"

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

    @model_validator(mode="after")
    def _validate_retry_window(self) -> Settings:
        if self.substack_retry_max_wait_sec < self.substack_retry_min_wait_sec:
            raise ValueError(
                "substack_retry_max_wait_sec must be greater than or equal to "
                "substack_retry_min_wait_sec"
            )
        return self


settings = Settings()
