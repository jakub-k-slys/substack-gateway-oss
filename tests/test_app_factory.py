from __future__ import annotations

from gateway_oss.app_factory import _get_application_info
from gateway_oss.extensions.base import ApplicationInfo


def test_get_application_info_normalizes_features(monkeypatch) -> None:
    class Runtime:
        application_info = ApplicationInfo(
            application="substack-gateway",
            tier="pro",
            version="0.11.0",
            features=("mcp:notes:create", "api:notes:create", "mcp:notes:create"),
        )

    monkeypatch.setattr("gateway_oss.app_factory.get_runtime", lambda: Runtime())

    info = _get_application_info()

    assert info.application == "substack-gateway"
    assert info.tier == "pro"
    assert info.version == "0.11.0"
    assert info.features == ("api:notes:create", "mcp:notes:create")
