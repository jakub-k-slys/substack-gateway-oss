from __future__ import annotations

from gateway_oss.extensions.base import ModuleInfo
from substack_gateway.app_factory import _build_modules


def test_build_modules_includes_oss_and_normalizes_features(monkeypatch) -> None:
    extra = ModuleInfo(
        name="gateway-extra",
        version="0.11.0",
        features=("mcp:notes:create", "api:notes:create", "mcp:notes:create"),
    )

    class Runtime:
        module_infos = [extra]

    monkeypatch.setattr("substack_gateway.app_factory.get_runtime", lambda: Runtime())

    modules = {module.name: module for module in _build_modules()}

    assert "gateway-oss" in modules
    extra_mod = modules["gateway-extra"]
    assert extra_mod.version == "0.11.0"
    assert extra_mod.features == ("api:notes:create", "mcp:notes:create")
