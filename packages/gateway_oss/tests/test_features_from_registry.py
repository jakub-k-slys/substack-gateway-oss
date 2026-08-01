from __future__ import annotations

from starlette.testclient import TestClient

from gateway_oss.app_factory import create_app


def test_root_reports_notes_features_from_registry() -> None:
    with TestClient(create_app()) as client:
        body = client.get("/").json()
    oss = next(m for m in body["modules"] if m["name"] == "gateway-oss")
    for feat in ("api:notes:create", "mcp:notes:create", "api:notes:get"):
        assert feat in oss["features"]
