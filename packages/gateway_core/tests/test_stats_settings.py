from __future__ import annotations

import pytest

from gateway_core.config import Settings


def test_stats_defaults() -> None:
    s = Settings()
    assert s.stats_timeseries_watermark_lag_days == 2


def test_stats_settings_read_native_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUBSTACK_GATEWAY_STATS_TIMESERIES_WATERMARK_LAG_DAYS", "0")
    s = Settings()
    assert s.stats_timeseries_watermark_lag_days == 0


def test_watermark_lag_rejects_negative(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUBSTACK_GATEWAY_STATS_TIMESERIES_WATERMARK_LAG_DAYS", "-1")
    with pytest.raises(ValueError):
        Settings()
