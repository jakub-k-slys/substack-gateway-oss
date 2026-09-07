from __future__ import annotations

from starlette.testclient import TestClient

from gateway_oss import create_app


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


def test_root_reports_drafts_features_from_registry() -> None:
    with TestClient(create_app()) as client:
        body = client.get("/").json()
    oss = next(m for m in body["modules"] if m["name"] == "gateway-oss")
    for feat in (
        "api:drafts:list",
        "api:drafts:get",
        "api:drafts:create",
        "api:drafts:update",
        "api:drafts:delete",
        "api:drafts:schedule",
        "api:drafts:unschedule",
        "api:drafts:prepublish",
        "api:drafts:ai-detection",
        "api:images:create",
        "mcp:drafts:list",
        "mcp:drafts:get",
        "mcp:drafts:create",
        "mcp:drafts:update",
        "mcp:drafts:delete",
        "mcp:drafts:schedule",
        "mcp:drafts:unschedule",
        "mcp:drafts:prepublish",
        "mcp:drafts:ai-detection",
        "mcp:images:upload",
    ):
        assert feat in oss["features"]


def test_root_reports_stats_features_from_registry() -> None:
    with TestClient(create_app()) as client:
        body = client.get("/").json()
    oss = next(m for m in body["modules"] if m["name"] == "gateway-oss")
    for feat in (
        "api:stats:subscribers",
        "api:stats:traffic:30d-views",
        "api:posts:stats:engagement",
        "api:posts:stats:traffic",
        "api:posts:stats:recipients",
        "api:posts:stats:growth",
        "api:posts:stats:discussion",
        "mcp:stats:subscribers",
        "mcp:stats:traffic:30d-views",
        "mcp:posts:stats:engagement",
        "mcp:posts:stats:traffic",
        "mcp:posts:stats:recipients",
        "mcp:posts:stats:growth",
        "mcp:posts:stats:discussion",
    ):
        assert feat in oss["features"]


def test_root_reports_posts_engagement_features_from_registry() -> None:
    with TestClient(create_app()) as client:
        body = client.get("/").json()
    oss = next(m for m in body["modules"] if m["name"] == "gateway-oss")
    for feat in (
        "api:posts:like",
        "api:posts:unlike",
        "api:posts:restack",
        "mcp:posts:like",
        "mcp:posts:unlike",
        "mcp:posts:restack",
    ):
        assert feat in oss["features"]
