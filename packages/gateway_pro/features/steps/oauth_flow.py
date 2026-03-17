"""Step definitions for the OAuth three-phase login flow.

Uses in-memory dictionary-backed mock repositories so no real database
is required.
"""

from __future__ import annotations

import base64
import json
import types
from datetime import datetime, timedelta, timezone

import bcrypt
from behave import given, then, when
from gateway_pro.oauth.db import (
    DBAuthCode,
    DBAuthRequest,
    DBLoginSession,
    DBUser,
    DBUserCredential,
)

_UTC = timezone.utc

_VALID_TOKEN = base64.b64encode(
    json.dumps({"substack_sid": "sid-val", "connect_sid": "csid-val"}).encode()
).decode()


# ---------------------------------------------------------------------------
# In-memory store and mock repositories
# ---------------------------------------------------------------------------


class InMemoryStore:
    def __init__(self) -> None:
        self.users: dict[int, DBUser] = {}
        self.users_by_email: dict[str, DBUser] = {}
        self.auth_requests: dict[str, DBAuthRequest] = {}
        self.login_sessions: dict[str, DBLoginSession] = {}
        self.user_credentials: dict[int, DBUserCredential] = {}
        self.auth_codes: dict[str, DBAuthCode] = {}
        self._user_seq = 0

    def add_user(self, email: str, password: str) -> DBUser:
        self._user_seq += 1
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = DBUser(id=self._user_seq, email=email, hashed_password=hashed)
        self.users[user.id] = user
        self.users_by_email[email] = user
        return user

    def add_auth_request(self, request_id: str, client_id: str) -> DBAuthRequest:
        req = DBAuthRequest(
            request_id=request_id,
            client_id=client_id,
            code_challenge="challenge123",
            redirect_uri="http://localhost/callback",
            redirect_uri_provided_explicitly=True,
            scopes="read",
            state="some-state",
            resource=None,
            expires_at=datetime.now(_UTC) + timedelta(seconds=600),
        )
        self.auth_requests[request_id] = req
        return req


class _MockUsers:
    def __init__(self, s: InMemoryStore) -> None:
        self._s = s

    async def get_by_email(self, email: str) -> DBUser | None:
        return self._s.users_by_email.get(email)

    async def save(self, user: DBUser) -> None:
        self._s.users[user.id] = user
        self._s.users_by_email[user.email] = user


class _MockAuthRequests:
    def __init__(self, s: InMemoryStore) -> None:
        self._s = s

    async def get(self, request_id: str) -> DBAuthRequest | None:
        return self._s.auth_requests.get(request_id)

    async def save(self, req: DBAuthRequest) -> None:
        self._s.auth_requests[req.request_id] = req

    async def delete(self, request_id: str) -> None:
        self._s.auth_requests.pop(request_id, None)


class _MockLoginSessions:
    def __init__(self, s: InMemoryStore) -> None:
        self._s = s

    async def get(self, session_id: str) -> DBLoginSession | None:
        return self._s.login_sessions.get(session_id)

    async def save(self, sess: DBLoginSession) -> None:
        self._s.login_sessions[sess.session_id] = sess

    async def delete(self, session_id: str) -> None:
        self._s.login_sessions.pop(session_id, None)


class _MockUserCredentials:
    def __init__(self, s: InMemoryStore) -> None:
        self._s = s

    async def get(self, user_id: int) -> DBUserCredential | None:
        return self._s.user_credentials.get(user_id)

    async def upsert(self, user_id: int, bearer: str, pub_url: str) -> None:
        self._s.user_credentials[user_id] = DBUserCredential(
            user_id=user_id, bearer=bearer, pub_url=pub_url
        )


class _MockAuthCodes:
    def __init__(self, s: InMemoryStore) -> None:
        self._s = s

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
# Given steps
# ---------------------------------------------------------------------------


@given('a registered gateway user "{email}" with password "{password}"')
def step_register_user(context, email, password):
    if not hasattr(context, "oauth_store"):
        context.oauth_store = InMemoryStore()
    context.oauth_store.add_user(email, password)

    # Patch UnitOfWork in the actual login module (not the re-export wrapper)
    import gateway_pro.oauth.login as login_mod
    from gateway_oss.config import settings

    store = context.oauth_store
    context._original_uow = getattr(login_mod, "UnitOfWork")
    login_mod.UnitOfWork = lambda: MockUnitOfWork(store)

    context._original_base_url = settings.base_url
    settings.base_url = "http://localhost"


@given('a valid OAuth auth request "{request_id}" for client "{client_id}"')
def step_create_auth_request(context, request_id, client_id):
    context.oauth_store.add_auth_request(request_id, client_id)


@given('the auth request "{request_id}" has expired')
def step_expire_auth_request(context, request_id):
    context.oauth_store.auth_requests[request_id].expires_at = datetime.now(
        _UTC
    ) - timedelta(seconds=1)


@given('I have completed phase 1 login with "{email}" and "{password}"')
def step_complete_phase1(context, email, password):
    resp = context.client.post(
        "/login/",
        data={"request_id": "test-req-id", "email": email, "password": password},
        follow_redirects=False,
    )
    assert resp.status_code == 302, (
        f"Phase 1 login failed with status {resp.status_code}: {resp.text}"
    )
    context.session_id = resp.headers["location"].split("session_id=")[1]


@given("the login session has expired")
def step_expire_login_session(context):
    context.oauth_store.login_sessions[context.session_id].expires_at = datetime.now(
        _UTC
    ) - timedelta(seconds=1)


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when(
    'I submit the login form with email "{email}" and password "{password}" for request "{request_id}"'
)
def step_submit_login(context, email, password, request_id):
    context.response = context.client.post(
        "/login/",
        data={"request_id": request_id, "email": email, "password": password},
        follow_redirects=False,
    )


@when(
    'I submit the login form with empty email and password for request "{request_id}"'
)
def step_submit_login_empty(context, request_id):
    context.response = context.client.post(
        "/login/",
        data={"request_id": request_id, "email": "", "password": ""},
        follow_redirects=False,
    )


@when(
    'I submit the token form with a valid Substack token and publication URL "{pub_url}"'
)
def step_submit_valid_token(context, pub_url):
    context.response = context.client.post(
        "/login/token/",
        data={
            "session_id": context.session_id,
            "token": _VALID_TOKEN,
            "pub_url": pub_url,
        },
    )


@when('I submit the token form with token "{token}" and publication URL "{pub_url}"')
def step_submit_custom_token(context, token, pub_url):
    context.response = context.client.post(
        "/login/token/",
        data={
            "session_id": context.session_id,
            "token": token,
            "pub_url": pub_url,
        },
    )


@when('I visit the login page with request_id "{request_id}"')
def step_visit_login(context, request_id):
    context.response = context.client.get(f"/login?request_id={request_id}")


@when('I visit the token form with session_id "{session_id}"')
def step_visit_token_form(context, session_id):
    context.response = context.client.get(f"/login/token?session_id={session_id}")


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then('the redirect location contains "{fragment}"')
def step_redirect_contains(context, fragment):
    location = context.response.headers.get("location", "")
    assert fragment in location, (
        f'Expected redirect to contain "{fragment}", got "{location}"'
    )


@then('the response body contains "{text}"')
def step_body_contains(context, text):
    body = context.response.text
    assert text in body, f'Expected body to contain "{text}"'


@then('the response body does not contain "{text}"')
def step_body_not_contains(context, text):
    body = context.response.text
    assert text not in body, f'Expected body NOT to contain "{text}", but it does'


@then('the response body starts with "{prefix}"')
def step_body_starts_with(context, prefix):
    body = context.response.text
    assert body.startswith(prefix), (
        f'Expected body to start with "{prefix}", got "{body[:80]}"'
    )


@then("the success page has a styled button link")
def step_has_btn(context):
    body = context.response.text
    assert 'class="btn"' in body, "Expected a .btn link in the success page"
    assert "href=" in body, "Expected an href in the success page"


@then('the user credentials are stored with publication URL "{pub_url}"')
def step_credentials_stored(context, pub_url):
    creds = context.oauth_store.user_credentials
    assert len(creds) >= 1, "No credentials stored"
    cred = next(iter(creds.values()))
    assert cred.bearer == _VALID_TOKEN
    assert cred.pub_url == pub_url


@then('an auth code is created for client "{client_id}"')
def step_auth_code_created(context, client_id):
    codes = context.oauth_store.auth_codes
    assert len(codes) == 1, f"Expected 1 auth code, got {len(codes)}"
    code = next(iter(codes.values()))
    assert code.client_id == client_id


@then("the login session is deleted")
def step_session_deleted(context):
    assert len(context.oauth_store.login_sessions) == 0, "Login session was not deleted"


@then("the auth request is deleted")
def step_auth_request_deleted(context):
    assert len(context.oauth_store.auth_requests) == 0, "Auth request was not deleted"
