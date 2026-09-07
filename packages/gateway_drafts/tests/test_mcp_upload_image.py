from __future__ import annotations

import base64
import contextlib

import pytest

from gateway_drafts_mcp import tools as mcp_tools


class _FakeResp:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def json(self) -> dict:
        return self._payload


class _FakePub:
    def __init__(self, payload: dict) -> None:
        self._payload = payload
        self.calls: list[dict] = []

    async def post(self, path: str, json: dict | None = None):
        self.calls.append({"path": path, "json": json})
        return _FakeResp(self._payload)


_RESPONSE = {
    "id": 1,
    "url": "https://substack-post-media.s3.amazonaws.com/x.png",
    "contentType": "image/png",
    "bytes": 3,
    "imageWidth": 10,
    "imageHeight": 20,
}


@pytest.mark.anyio
async def test_upload_image_tool_uploads_and_returns_result(monkeypatch) -> None:
    pub = _FakePub(_RESPONSE)

    @contextlib.asynccontextmanager
    async def _fake_clients(token: str):
        yield (pub, object())

    monkeypatch.setattr(mcp_tools, "_authenticated_clients", _fake_clients)

    result = await mcp_tools.upload_image(
        token="tok", image_base64=base64.b64encode(b"ABC").decode()
    )

    assert pub.calls == [
        {"path": "image", "json": {"image": "data:image/png;base64,QUJD"}}
    ]
    assert result["url"] == "https://substack-post-media.s3.amazonaws.com/x.png"
    assert result["width"] == 10
    assert result["content_type"] == "image/png"
