from __future__ import annotations

from gateway_core.capabilities import McpCapability, RestCapability


def test_rest_capability_defaults() -> None:
    cap = RestCapability(domain="notes", router=object())  # ty: ignore[invalid-argument-type]
    assert cap.mount_prefix == "/v1"
    assert cap.features == ()


def test_mcp_capability_holds_register_callable() -> None:
    calls: list[object] = []
    cap = McpCapability(
        domain="notes", register=calls.append, features=("mcp:notes:get",)
    )
    cap.register("server")  # ty: ignore[invalid-argument-type]
    assert calls == ["server"]
    assert cap.features == ("mcp:notes:get",)
