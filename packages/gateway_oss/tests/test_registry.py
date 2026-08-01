from __future__ import annotations

from gateway_core.capabilities import McpCapability, RestCapability
from gateway_oss import registry


class _FakeEP:
    def __init__(self, obj: object) -> None:
        self._obj = obj

    def load(self):
        return lambda: self._obj


def test_load_splits_rest_and_mcp(monkeypatch) -> None:
    rest = RestCapability(domain="notes", router=object())  # ty: ignore[invalid-argument-type]
    mcp = McpCapability(domain="notes", register=lambda s: None)
    monkeypatch.setattr(
        registry.importlib.metadata,
        "entry_points",
        lambda group: [_FakeEP(rest), _FakeEP(mcp)],
    )
    assert registry.load_rest_capabilities() == [rest]
    assert registry.load_mcp_capabilities() == [mcp]
