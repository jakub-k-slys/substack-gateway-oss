from __future__ import annotations

import pytest

from gateway_core.config import Settings


def test_stats_defaults() -> None:
    s = Settings()
    assert s.stats_snapshot_cache_ttl_sec == 900
    assert s.stats_timeseries_ttl_sec == 86_400
    assert s.stats_timeseries_watermark_lag_days == 2


def test_stats_settings_read_native_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUBSTACK_GATEWAY_STATS_SNAPSHOT_CACHE_TTL_SEC", "60")
    monkeypatch.setenv("SUBSTACK_GATEWAY_STATS_TIMESERIES_TTL_SEC", "120")
    monkeypatch.setenv("SUBSTACK_GATEWAY_STATS_TIMESERIES_WATERMARK_LAG_DAYS", "0")
    s = Settings()
    assert s.stats_snapshot_cache_ttl_sec == 60
    assert s.stats_timeseries_ttl_sec == 120
    assert s.stats_timeseries_watermark_lag_days == 0


def test_stats_ttls_reject_non_positive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUBSTACK_GATEWAY_STATS_SNAPSHOT_CACHE_TTL_SEC", "0")
    with pytest.raises(ValueError):
        Settings()


def test_watermark_lag_rejects_negative(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUBSTACK_GATEWAY_STATS_TIMESERIES_WATERMARK_LAG_DAYS", "-1")
    with pytest.raises(ValueError):
        Settings()
