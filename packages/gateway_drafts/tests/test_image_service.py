from __future__ import annotations

from typing import cast

import pytest

from gateway_core.client.publication import PublicationClient
from gateway_drafts.image import ImagesService


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
    "id": 303467639,
    "url": "https://substack-post-media.s3.amazonaws.com/public/images/e175.png",
    "contentType": "image/png",
    "bytes": 72180,
    "imageWidth": 2387,
    "imageHeight": 203,
}


@pytest.mark.anyio
async def test_upload_posts_the_image_field_and_normalizes_response() -> None:
    pub = _FakePub(_RESPONSE)
    result = await ImagesService(cast(PublicationClient, pub)).upload(
        "data:image/png;base64,QUJD"
    )

    assert pub.calls == [
        {"path": "image", "json": {"image": "data:image/png;base64,QUJD"}}
    ]
    assert result.id == 303467639
    assert result.url == _RESPONSE["url"]
    assert result.width == 2387
    assert result.height == 203
    assert result.bytes == 72180
    assert result.content_type == "image/png"
