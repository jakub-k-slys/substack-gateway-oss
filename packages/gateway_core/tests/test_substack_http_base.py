from __future__ import annotations

import logging

import httpx
import pytest
import respx

from gateway_core.client.base import SubstackHTTPBase
from gateway_core.client.exceptions import SubstackAPIError, SubstackAuthError

_BASE = "https://example.com/api/v1"


class _TestClient(SubstackHTTPBase):
    _base = _BASE


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
@pytest.mark.parametrize("status", [408, 425, 429, 500, 502, 503, 504])
async def test_single_request_on_status(status: int) -> None:
    with respx.mock(assert_all_mocked=True) as mock:
        route = mock.get(f"{_BASE}/posts").respond(status, json={"message": "nope"})

        async with _TestClient("sid", "connect") as client:
            with pytest.raises(SubstackAPIError) as excinfo:
                await client.get("posts")

    assert route.call_count == 1
    assert excinfo.value.status_code == status


@pytest.mark.anyio
async def test_single_request_on_connect_error() -> None:
    with respx.mock(assert_all_mocked=True) as mock:
        route = mock.get(f"{_BASE}/posts").mock(
            side_effect=httpx.ConnectError("refused")
        )

        async with _TestClient("sid", "connect") as client:
            with pytest.raises(SubstackAPIError, match="Network error") as excinfo:
                await client.get("posts")

    assert route.call_count == 1
    assert excinfo.value.status_code == 502


@pytest.mark.anyio
async def test_post_single_request_on_429() -> None:
    with respx.mock(assert_all_mocked=True) as mock:
        route = mock.post(f"{_BASE}/notes").respond(429, json={})

        async with _TestClient("sid", "connect") as client:
            with pytest.raises(SubstackAPIError) as excinfo:
                await client.post("notes", json={"body": "hi"})

    assert route.call_count == 1
    assert excinfo.value.status_code == 429


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("status", "message"),
    [
        (401, "Invalid or expired Substack session token"),
        (403, "Forbidden: insufficient permissions for this resource"),
    ],
)
async def test_401_403_auth_error(status: int, message: str) -> None:
    with respx.mock(assert_all_mocked=True) as mock:
        route = mock.get(f"{_BASE}/posts").respond(status, json={"message": "no"})

        async with _TestClient("sid", "connect") as client:
            with pytest.raises(SubstackAuthError) as excinfo:
                await client.get("posts")

    assert route.call_count == 1
    assert excinfo.value.status_code == status
    assert message in str(excinfo.value)


@pytest.mark.anyio
async def test_404_api_error_detail_from_body() -> None:
    with respx.mock(assert_all_mocked=True) as mock:
        mock.get(f"{_BASE}/posts/1").respond(404, json={"error": "Post not found"})

        async with _TestClient("sid", "connect") as client:
            with pytest.raises(
                SubstackAPIError, match="Substack returned 404: Post not found"
            ) as excinfo:
                await client.get("posts/1")

    assert excinfo.value.status_code == 404


@pytest.mark.anyio
async def test_success_returns_response() -> None:
    with respx.mock(assert_all_mocked=True) as mock:
        route = mock.get(f"{_BASE}/posts").respond(200, json={"ok": True})

        async with _TestClient("sid", "connect") as client:
            response = await client.get("posts")

    assert route.call_count == 1
    assert response.json() == {"ok": True}


@pytest.mark.anyio
async def test_network_error_is_logged_once(caplog: pytest.LogCaptureFixture) -> None:
    with respx.mock(assert_all_mocked=True) as mock:
        mock.get(f"{_BASE}/posts").mock(side_effect=httpx.ReadTimeout("timed out"))

        with caplog.at_level(logging.WARNING, logger="gateway_core.client.base"):
            async with _TestClient("sid", "connect", request_id="rid") as client:
                with pytest.raises(SubstackAPIError, match="Network error: timed out"):
                    await client.get("posts")

    messages = [
        r.getMessage() for r in caplog.records if r.name == "gateway_core.client.base"
    ]
    assert len(messages) == 1
    assert messages[0].startswith("[rid] Substack network error: GET ")
    assert "timed out" in messages[0]
