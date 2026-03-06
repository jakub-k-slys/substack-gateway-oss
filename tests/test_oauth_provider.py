"""Unit tests for gateway.oauth.provider.

Covers:
  - _encode_bearer / _validate_bearer helpers
  - _issue_jwt payload structure
  - Login form HTML rendering (no DB required)
  - Login form field-validation error paths (no DB required)
  - POST /api/v1/users endpoint — non-DB error paths
"""

from __future__ import annotations

import base64
import json

import jwt
import pytest
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.testclient import TestClient

from gateway.oauth.bearer import _encode_bearer, _validate_bearer
from gateway.oauth.provider import NeonOAuthProvider

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_BASE_URL = "http://localhost/mcp"
_JWT_SECRET = "test-only-secret"


@pytest.fixture()
def provider(monkeypatch):
    monkeypatch.setattr("gateway.config.settings.jwt_secret", _JWT_SECRET)
    return NeonOAuthProvider(base_url=_BASE_URL)


@pytest.fixture()
def login_client(provider):
    """Minimal Starlette app exposing only the /login and /login/token routes."""
    all_routes = provider.get_routes()
    routes = [
        r
        for r in all_routes
        if isinstance(r, Route) and r.path in ("/login", "/login/token")
    ]
    app = Starlette(routes=routes)
    return TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# _encode_bearer
# ---------------------------------------------------------------------------


class TestEncodeBearer:
    def test_produces_valid_base64_json(self):
        bearer = _encode_bearer("sid-value", "csid-value")
        decoded = json.loads(base64.b64decode(bearer))
        assert decoded["substack_sid"] == "sid-value"
        assert decoded["connect_sid"] == "csid-value"

    def test_roundtrip_with_validate(self):
        bearer = _encode_bearer("s", "c")
        _validate_bearer(bearer)  # should not raise

    def test_different_inputs_produce_different_tokens(self):
        a = _encode_bearer("sid1", "csid1")
        b = _encode_bearer("sid2", "csid2")
        assert a != b


# ---------------------------------------------------------------------------
# _validate_bearer
# ---------------------------------------------------------------------------


class TestValidateBearer:
    def test_valid_bearer_passes(self):
        bearer = _encode_bearer("sid", "csid")
        _validate_bearer(bearer)  # no exception

    def test_missing_substack_sid_raises(self):
        payload = base64.b64encode(json.dumps({"connect_sid": "x"}).encode()).decode()
        with pytest.raises(ValueError, match="substack_sid"):
            _validate_bearer(payload)

    def test_missing_connect_sid_raises(self):
        payload = base64.b64encode(json.dumps({"substack_sid": "x"}).encode()).decode()
        with pytest.raises(ValueError, match="connect_sid"):
            _validate_bearer(payload)

    def test_empty_substack_sid_raises(self):
        payload = base64.b64encode(
            json.dumps({"substack_sid": "", "connect_sid": "x"}).encode()
        ).decode()
        with pytest.raises(ValueError, match="substack_sid"):
            _validate_bearer(payload)

    def test_invalid_base64_raises(self):
        with pytest.raises(ValueError):
            _validate_bearer("not-valid-base64!!!")

    def test_non_json_raises(self):
        payload = base64.b64encode(b"hello world").decode()
        with pytest.raises(ValueError):
            _validate_bearer(payload)


# ---------------------------------------------------------------------------
# _issue_jwt
# ---------------------------------------------------------------------------


class TestIssueJwt:
    def test_jwt_contains_expected_claims(self, provider):
        token, jti, exp = provider._issue_jwt("client-abc", ["read", "write"])
        payload = jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        assert payload["client_id"] == "client-abc"
        assert payload["scope"] == "read write"
        assert payload["jti"] == jti
        assert payload["exp"] == exp
        assert "user_id" not in payload

    def test_jwt_includes_user_id_when_provided(self, provider):
        token, _, _ = provider._issue_jwt("client-abc", [], user_id=99)
        payload = jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        assert payload["user_id"] == 99

    def test_jwt_user_id_none_omits_field(self, provider):
        token, _, _ = provider._issue_jwt("client-abc", [], user_id=None)
        payload = jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        assert "user_id" not in payload

    def test_each_call_produces_unique_jti(self, provider):
        _, jti1, _ = provider._issue_jwt("c", [])
        _, jti2, _ = provider._issue_jwt("c", [])
        assert jti1 != jti2

    def test_exp_is_in_future(self, provider):
        import time

        _, _, exp = provider._issue_jwt("c", [])
        assert exp > int(time.time())


# ---------------------------------------------------------------------------
# Login form HTML — phase 1
# ---------------------------------------------------------------------------


class TestLoginForm:
    def test_get_returns_200(self, login_client):
        response = login_client.get("/login?request_id=test-rid")
        assert response.status_code == 200

    def test_form_shows_step_1_of_2(self, login_client):
        response = login_client.get("/login?request_id=rid")
        assert "Step 1 of 2" in response.text

    def test_form_contains_email_and_password_fields(self, login_client):
        response = login_client.get("/login?request_id=rid")
        assert 'name="email"' in response.text
        assert 'name="password"' in response.text

    def test_request_id_is_embedded_in_form(self, login_client):
        response = login_client.get("/login?request_id=my-request-id")
        assert "my-request-id" in response.text

    def test_get_without_request_id_still_renders(self, login_client):
        response = login_client.get("/login")
        assert response.status_code == 200

    def test_post_with_empty_fields_shows_error(self, login_client):
        response = login_client.post(
            "/login",
            data={"request_id": "rid", "email": "", "password": ""},
        )
        assert response.status_code == 200
        assert "All fields are required" in response.text

    def test_post_with_missing_request_id_shows_error(self, login_client):
        response = login_client.post(
            "/login",
            data={"request_id": "", "email": "a@b.com", "password": "pw"},
        )
        assert response.status_code == 200
        assert "All fields are required" in response.text

    def test_xss_in_request_id_is_escaped(self, login_client):
        response = login_client.get("/login?request_id=<script>alert(1)</script>")
        assert "<script>" not in response.text


# ---------------------------------------------------------------------------
# Token form HTML — phase 2
# ---------------------------------------------------------------------------


class TestTokenForm:
    def test_get_returns_200(self, login_client):
        response = login_client.get("/login/token?session_id=test-sid")
        assert response.status_code == 200

    def test_form_shows_step_2_of_2(self, login_client):
        response = login_client.get("/login/token?session_id=sid")
        assert "Step 2 of 2" in response.text

    def test_form_contains_cookie_fields(self, login_client):
        response = login_client.get("/login/token?session_id=sid")
        assert 'name="substack_sid"' in response.text
        assert 'name="connect_sid"' in response.text
        assert 'name="pub_url"' in response.text

    def test_session_id_is_embedded_in_form(self, login_client):
        response = login_client.get("/login/token?session_id=my-session-id")
        assert "my-session-id" in response.text

    def test_post_with_empty_fields_shows_error(self, login_client):
        response = login_client.post(
            "/login/token",
            data={
                "session_id": "sid",
                "substack_sid": "",
                "connect_sid": "",
                "pub_url": "",
            },
        )
        assert response.status_code == 200
        assert "All fields are required" in response.text

    def test_xss_in_session_id_is_escaped(self, login_client):
        response = login_client.get("/login/token?session_id=<script>alert(1)</script>")
        assert "<script>" not in response.text


# ---------------------------------------------------------------------------
# POST /api/v1/users — non-DB error paths
# ---------------------------------------------------------------------------

_VALID_INIT_TOKEN = (
    "WW91IHNoYWxsIG5vdCBwYXNzLiBZb3Ugc2hhbGwgbm90IHBhc3MsIHlvdSBzaGFsbCBub3QgcGFzcyEK"
)


@pytest.fixture(scope="module")
def api_client():
    from main import app

    return TestClient(app, raise_server_exceptions=False)


class TestCreateUserEndpoint:
    def test_missing_token_query_param_returns_422(self, api_client):
        response = api_client.post(
            "/api/v1/users", json={"email": "a@b.com", "password": "pw"}
        )
        assert response.status_code == 422

    def test_wrong_token_returns_403(self, api_client):
        response = api_client.post(
            "/api/v1/users?token=wrong-token",
            json={"email": "a@b.com", "password": "pw"},
        )
        assert response.status_code == 403
        assert "Invalid token" in response.json()["detail"]

    def test_correct_token_without_oauth_configured_returns_503(self, api_client):
        # In test env DATABASE_URL is not set → oauth_enabled is False
        response = api_client.post(
            f"/api/v1/users?token={_VALID_INIT_TOKEN}",
            json={"email": "a@b.com", "password": "pw"},
        )
        assert response.status_code == 503

    def test_create_user_with_mocked_db(self, monkeypatch):
        """201 path with all DB calls mocked out."""
        import importlib
        from unittest.mock import AsyncMock, MagicMock

        users_mod = importlib.import_module("gateway.api.v1.users")
        from gateway.config import settings

        mock_conn = AsyncMock()
        mock_engine = MagicMock()
        mock_engine.begin.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_engine.begin.return_value.__aexit__ = AsyncMock(return_value=False)

        monkeypatch.setattr(settings, "database_url", "postgresql+asyncpg://fake")
        monkeypatch.setattr(settings, "base_url", "http://localhost")
        monkeypatch.setattr(settings, "jwt_secret", "test-secret")
        monkeypatch.setattr(users_mod, "get_engine", lambda: mock_engine)
        monkeypatch.setattr(users_mod, "init_db", AsyncMock())

        from main import app

        client = TestClient(app, raise_server_exceptions=False)
        response = client.post(
            f"/api/v1/users?token={_VALID_INIT_TOKEN}",
            json={"email": "New@Example.com", "password": "secret123"},
        )
        assert response.status_code == 201
        assert response.json()["email"] == "new@example.com"

    def test_duplicate_email_returns_409(self, monkeypatch):
        """409 when the DB raises a unique constraint violation."""
        import importlib
        from unittest.mock import AsyncMock, MagicMock

        users_mod = importlib.import_module("gateway.api.v1.users")
        from gateway.config import settings

        mock_conn = AsyncMock()
        mock_conn.execute.side_effect = Exception("unique constraint violation")
        mock_engine = MagicMock()
        mock_engine.begin.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_engine.begin.return_value.__aexit__ = AsyncMock(return_value=False)

        monkeypatch.setattr(settings, "database_url", "postgresql+asyncpg://fake")
        monkeypatch.setattr(settings, "base_url", "http://localhost")
        monkeypatch.setattr(settings, "jwt_secret", "test-secret")
        monkeypatch.setattr(users_mod, "get_engine", lambda: mock_engine)
        monkeypatch.setattr(users_mod, "init_db", AsyncMock())

        from main import app

        client = TestClient(app, raise_server_exceptions=False)
        response = client.post(
            f"/api/v1/users?token={_VALID_INIT_TOKEN}",
            json={"email": "existing@example.com", "password": "pw"},
        )
        assert response.status_code == 409
