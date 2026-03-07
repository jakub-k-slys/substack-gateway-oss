"""Full OAuth login flow tests with in-memory mock repositories.

Walks through all three phases of the login flow:
  Phase 1 — email + password → login session + redirect
  Phase 2 — Substack bearer token → auth code + success page
  Phase 3 — success page renders button (no JS redirect)

Also covers:
  - Doctype rendering (no HTML-escaped <!doctype html>)
  - Error paths across phases
"""

from __future__ import annotations

import base64
import json
import types
from datetime import datetime, timedelta, timezone

import bcrypt
import pytest
from fastapi.testclient import TestClient

from gateway.oauth.db import (
    DBAuthCode,
    DBAuthRequest,
    DBLoginSession,
    DBUser,
    DBUserCredential,
)

_UTC = timezone.utc

# ---------------------------------------------------------------------------
# In-memory store
# ---------------------------------------------------------------------------

_VALID_TOKEN = base64.b64encode(
    json.dumps({"substack_sid": "sid-val", "connect_sid": "csid-val"}).encode()
).decode()
_PUB_URL = "https://test.substack.com"
_TEST_EMAIL = "user@example.com"
_TEST_PASSWORD = "secret123"
_HASHED_PW = bcrypt.hashpw(_TEST_PASSWORD.encode(), bcrypt.gensalt()).decode()


class InMemoryStore:
    """Shared mutable state backing all mock repositories."""

    def __init__(self) -> None:
        self.users: dict[int, DBUser] = {}
        self.users_by_email: dict[str, DBUser] = {}
        self.auth_requests: dict[str, DBAuthRequest] = {}
        self.login_sessions: dict[str, DBLoginSession] = {}
        self.user_credentials: dict[int, DBUserCredential] = {}
        self.auth_codes: dict[str, DBAuthCode] = {}
        self._user_seq = 0

    def add_user(self, email: str, hashed_pw: str) -> DBUser:
        self._user_seq += 1
        user = DBUser(id=self._user_seq, email=email, hashed_password=hashed_pw)
        self.users[user.id] = user
        self.users_by_email[email] = user
        return user

    def add_auth_request(self, **kwargs) -> DBAuthRequest:
        req = DBAuthRequest(**kwargs)
        self.auth_requests[req.request_id] = req
        return req


# ---------------------------------------------------------------------------
# Mock repositories
# ---------------------------------------------------------------------------


class _MockUsers:
    def __init__(self, store: InMemoryStore) -> None:
        self._s = store

    async def get_by_email(self, email: str) -> DBUser | None:
        return self._s.users_by_email.get(email)

    async def save(self, user: DBUser) -> None:
        self._s.users[user.id] = user
        self._s.users_by_email[user.email] = user


class _MockAuthRequests:
    def __init__(self, store: InMemoryStore) -> None:
        self._s = store

    async def get(self, request_id: str) -> DBAuthRequest | None:
        return self._s.auth_requests.get(request_id)

    async def save(self, req: DBAuthRequest) -> None:
        self._s.auth_requests[req.request_id] = req

    async def delete(self, request_id: str) -> None:
        self._s.auth_requests.pop(request_id, None)


class _MockLoginSessions:
    def __init__(self, store: InMemoryStore) -> None:
        self._s = store

    async def get(self, session_id: str) -> DBLoginSession | None:
        return self._s.login_sessions.get(session_id)

    async def save(self, sess: DBLoginSession) -> None:
        self._s.login_sessions[sess.session_id] = sess

    async def delete(self, session_id: str) -> None:
        self._s.login_sessions.pop(session_id, None)


class _MockUserCredentials:
    def __init__(self, store: InMemoryStore) -> None:
        self._s = store

    async def get(self, user_id: int) -> DBUserCredential | None:
        return self._s.user_credentials.get(user_id)

    async def upsert(self, user_id: int, bearer: str, pub_url: str) -> None:
        self._s.user_credentials[user_id] = DBUserCredential(
            user_id=user_id, bearer=bearer, pub_url=pub_url
        )


class _MockAuthCodes:
    def __init__(self, store: InMemoryStore) -> None:
        self._s = store

    async def get(self, code: str, client_id: str) -> DBAuthCode | None:
        ac = self._s.auth_codes.get(code)
        if ac and ac.client_id == client_id:
            return ac
        return None

    async def save(self, auth_code: DBAuthCode) -> None:
        self._s.auth_codes[auth_code.code] = auth_code

    async def consume(self, code: str) -> int | None:
        ac = self._s.auth_codes.pop(code, None)
        return ac.user_id if ac else None


class MockUnitOfWork:
    """Drop-in replacement for UnitOfWork backed by an InMemoryStore."""

    def __init__(self, store: InMemoryStore) -> None:
        self._store = store

    async def __aenter__(self) -> MockUnitOfWork:
        self.users = _MockUsers(self._store)
        self.auth_requests = _MockAuthRequests(self._store)
        self.login_sessions = _MockLoginSessions(self._store)
        self.user_credentials = _MockUserCredentials(self._store)
        self.auth_codes = _MockAuthCodes(self._store)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        return None


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def store():
    return InMemoryStore()


@pytest.fixture()
def seeded_store(store):
    """Store pre-populated with a user and a valid auth request."""
    store.add_user(_TEST_EMAIL, _HASHED_PW)
    store.add_auth_request(
        request_id="test-req-id",
        client_id="test-client",
        code_challenge="challenge123",
        redirect_uri="http://localhost/callback",
        redirect_uri_provided_explicitly=True,
        scopes="read",
        state="some-state",
        resource=None,
        expires_at=datetime.now(_UTC) + timedelta(seconds=600),
    )
    return store


@pytest.fixture()
def client(seeded_store, monkeypatch):
    """TestClient with UnitOfWork patched to use in-memory store."""
    mock_uow_factory = lambda: MockUnitOfWork(seeded_store)  # noqa: E731

    import gateway.oauth.login as login_mod

    monkeypatch.setattr(login_mod, "UnitOfWork", mock_uow_factory)
    monkeypatch.setattr("gateway.config.settings.base_url", "http://localhost")

    from main import app

    return TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# Doctype rendering
# ---------------------------------------------------------------------------


class TestDoctypeRendering:
    def test_doctype_not_escaped_in_login_page(self, client):
        resp = client.get("/login?request_id=test-req-id")
        assert resp.status_code == 200
        assert resp.text.startswith("<!doctype html>")
        assert "&lt;!doctype html&gt;" not in resp.text

    def test_doctype_not_escaped_in_token_page(self, client):
        resp = client.get("/login/token?session_id=sid")
        assert resp.status_code == 200
        assert resp.text.startswith("<!doctype html>")
        assert "&lt;!doctype html&gt;" not in resp.text


# ---------------------------------------------------------------------------
# Full flow
# ---------------------------------------------------------------------------


class TestFullOAuthFlow:
    def test_phase1_wrong_password_shows_error(self, client):
        resp = client.post(
            "/login/",
            data={
                "request_id": "test-req-id",
                "email": _TEST_EMAIL,
                "password": "wrong",
            },
        )
        assert resp.status_code == 200
        assert "Invalid email or password" in resp.text

    def test_phase1_unknown_email_shows_error(self, client):
        resp = client.post(
            "/login/",
            data={
                "request_id": "test-req-id",
                "email": "nobody@example.com",
                "password": _TEST_PASSWORD,
            },
        )
        assert resp.status_code == 200
        assert "Invalid email or password" in resp.text

    def test_phase1_expired_auth_request_shows_error(self, client, seeded_store):
        seeded_store.auth_requests["test-req-id"].expires_at = datetime.now(
            _UTC
        ) - timedelta(seconds=1)
        resp = client.post(
            "/login/",
            data={
                "request_id": "test-req-id",
                "email": _TEST_EMAIL,
                "password": _TEST_PASSWORD,
            },
        )
        assert resp.status_code == 200
        assert "Session expired" in resp.text

    def _do_login(self, client):
        """Run phase 1 and return the session_id from the redirect."""
        resp = client.post(
            "/login/",
            data={
                "request_id": "test-req-id",
                "email": _TEST_EMAIL,
                "password": _TEST_PASSWORD,
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        return resp.headers["location"].split("session_id=")[1]

    def test_phase1_valid_login_redirects_to_token_form(self, client):
        resp = client.post(
            "/login/",
            data={
                "request_id": "test-req-id",
                "email": _TEST_EMAIL,
                "password": _TEST_PASSWORD,
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        location = resp.headers["location"]
        assert "/login/token?session_id=" in location

    def test_full_flow_phase1_then_phase2(self, client, seeded_store):
        session_id = self._do_login(client)

        # Phase 2 — submit token
        resp2 = client.post(
            "/login/token/",
            data={
                "session_id": session_id,
                "token": _VALID_TOKEN,
                "pub_url": _PUB_URL,
            },
        )
        assert resp2.status_code == 200

        # Phase 3 assertions — success page
        body = resp2.text
        assert "Step 3 of 3" in body
        assert "All done!" in body
        assert "Complete setup" in body

        # Must have a link, not a JS redirect
        assert "window.location" not in body
        assert "<script>" not in body
        assert 'class="btn"' in body
        assert "href=" in body

        # Redirect URL should include the auth code and state
        assert "code=" in body
        assert "state=some-state" in body

        # Doctype must not be escaped
        assert body.startswith("<!doctype html>")
        assert "&lt;!doctype html&gt;" not in body

    def test_phase2_stores_credentials(self, client, seeded_store):
        session_id = self._do_login(client)

        client.post(
            "/login/token/",
            data={
                "session_id": session_id,
                "token": _VALID_TOKEN,
                "pub_url": _PUB_URL,
            },
        )

        assert 1 in seeded_store.user_credentials
        cred = seeded_store.user_credentials[1]
        assert cred.bearer == _VALID_TOKEN
        assert cred.pub_url == _PUB_URL

    def test_phase2_creates_auth_code(self, client, seeded_store):
        session_id = self._do_login(client)

        client.post(
            "/login/token/",
            data={
                "session_id": session_id,
                "token": _VALID_TOKEN,
                "pub_url": _PUB_URL,
            },
        )

        assert len(seeded_store.auth_codes) == 1
        code = next(iter(seeded_store.auth_codes.values()))
        assert code.client_id == "test-client"
        assert code.user_id == 1

    def test_phase2_cleans_up_session_and_request(self, client, seeded_store):
        session_id = self._do_login(client)

        client.post(
            "/login/token/",
            data={
                "session_id": session_id,
                "token": _VALID_TOKEN,
                "pub_url": _PUB_URL,
            },
        )

        assert len(seeded_store.login_sessions) == 0
        assert len(seeded_store.auth_requests) == 0

    def test_phase2_invalid_token_shows_error(self, client, seeded_store):
        session_id = self._do_login(client)

        resp2 = client.post(
            "/login/token/",
            data={
                "session_id": session_id,
                "token": "not-valid-base64!!!",
                "pub_url": _PUB_URL,
            },
        )
        assert resp2.status_code == 200
        assert "Step 2 of 3" in resp2.text  # still on token form

    def test_phase2_expired_session_shows_error(self, client, seeded_store):
        session_id = self._do_login(client)

        seeded_store.login_sessions[session_id].expires_at = datetime.now(
            _UTC
        ) - timedelta(seconds=1)

        resp2 = client.post(
            "/login/token/",
            data={
                "session_id": session_id,
                "token": _VALID_TOKEN,
                "pub_url": _PUB_URL,
            },
        )
        assert resp2.status_code == 200
        assert "Session expired" in resp2.text


# ---------------------------------------------------------------------------
# Success page (render_success) unit tests
# ---------------------------------------------------------------------------


class TestRenderSuccess:
    def test_contains_redirect_link(self):
        from gateway.oauth.templates import render_success

        resp = render_success("http://example.com/callback?code=abc&state=xyz")
        body = resp.body.decode()
        assert 'href="http://example.com/callback?code=abc&amp;state=xyz"' in body

    def test_no_javascript(self):
        from gateway.oauth.templates import render_success

        resp = render_success("http://example.com/cb")
        body = resp.body.decode()
        assert "<script>" not in body
        assert "window.location" not in body

    def test_has_button_class(self):
        from gateway.oauth.templates import render_success

        resp = render_success("http://example.com/cb")
        body = resp.body.decode()
        assert 'class="btn"' in body
        assert "Complete setup" in body

    def test_doctype_correct(self):
        from gateway.oauth.templates import render_success

        resp = render_success("http://example.com/cb")
        body = resp.body.decode()
        assert body.startswith("<!doctype html>")
        assert "&lt;!doctype html&gt;" not in body
