from __future__ import annotations

from gateway_pro.config import ProSettings


def test_pro_settings_accepts_prefixed_env_names(monkeypatch) -> None:
    monkeypatch.setenv("SUBSTACK_GATEWAY_PRO_BASE_URL", "https://gateway.example")
    monkeypatch.setenv("SUBSTACK_GATEWAY_PRO_DATABASE_URL", "postgresql://db")
    monkeypatch.setenv("SUBSTACK_GATEWAY_PRO_JWT_SECRET", "secret")
    monkeypatch.setenv(
        "SUBSTACK_GATEWAY_PRO_FOLLOWING_FEED_PROFILE_CACHE_TTL_SEC", "42"
    )

    settings = ProSettings()

    assert settings.base_url == "https://gateway.example"
    assert settings.database_url == "postgresql://db"
    assert settings.jwt_secret == "secret"
    assert settings.following_feed_profile_cache_ttl_sec == 42
    assert settings.oauth_enabled is True


def test_pro_settings_accepts_legacy_env_names(monkeypatch) -> None:
    monkeypatch.setenv("SUBSTACK_GATEWAY_BASE_URL", "https://legacy.example")
    monkeypatch.setenv("SUBSTACK_GATEWAY_DATABASE_URL", "postgresql://legacy")
    monkeypatch.setenv("SUBSTACK_GATEWAY_JWT_SECRET", "legacy-secret")
    monkeypatch.setenv("SUBSTACK_GATEWAY_FOLLOWING_FEED_PROFILE_CACHE_TTL_SEC", "84")

    settings = ProSettings()

    assert settings.base_url == "https://legacy.example"
    assert settings.database_url == "postgresql://legacy"
    assert settings.jwt_secret == "legacy-secret"
    assert settings.following_feed_profile_cache_ttl_sec == 84
    assert settings.oauth_enabled is True
