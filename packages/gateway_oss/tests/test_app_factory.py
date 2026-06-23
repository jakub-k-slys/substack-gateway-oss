from __future__ import annotations

from gateway_oss.app_factory import _build_modules
from gateway_oss.extensions.base import ModuleInfo


def test_build_modules_includes_oss_and_normalizes_features(monkeypatch) -> None:
    extra = ModuleInfo(
        name="gateway-pro",
        version="0.11.0",
        features=("mcp:notes:create", "api:notes:create", "mcp:notes:create"),
    )

    class Runtime:
        module_infos = [extra]

    monkeypatch.setattr("gateway_oss.app_factory.get_runtime", lambda: Runtime())

    modules = {module.name: module for module in _build_modules()}

    assert "gateway-oss" in modules
    pro = modules["gateway-pro"]
    assert pro.version == "0.11.0"
    assert pro.features == ("api:notes:create", "mcp:notes:create")
