from __future__ import annotations

from starlette.testclient import TestClient

from gateway_oss.app_factory import create_app


def test_root_reports_notes_features_from_registry() -> None:
    with TestClient(create_app()) as client:
        body = client.get("/").json()
    oss = next(m for m in body["modules"] if m["name"] == "gateway-oss")
    for feat in ("api:notes:create", "mcp:notes:create", "api:notes:get"):
        assert feat in oss["features"]


def test_root_reports_posts_comments_following_features_from_registry() -> None:
    with TestClient(create_app()) as client:
        body = client.get("/").json()
    oss = next(m for m in body["modules"] if m["name"] == "gateway-oss")
    for feat in (
        "api:posts:get",
        "mcp:posts:get",
        "api:comments:get",
        "api:posts:comments:list",
        "mcp:posts:comments:list",
        "api:me:following:list",
        "mcp:me:following:list",
    ):
        assert feat in oss["features"]


def test_root_reports_profiles_me_features_from_registry() -> None:
    with TestClient(create_app()) as client:
        body = client.get("/").json()
    oss = next(m for m in body["modules"] if m["name"] == "gateway-oss")
    for feat in (
        "api:profiles:get",
        "api:profiles:posts:list",
        "api:profiles:notes:list",
        "mcp:profiles:get",
        "mcp:profiles:posts:list",
        "mcp:profiles:notes:list",
        "api:me:get",
        "api:me:notes:list",
        "api:me:posts:list",
        "mcp:me:get",
        "mcp:me:notes:list",
        "mcp:me:posts:list",
    ):
        assert feat in oss["features"]
