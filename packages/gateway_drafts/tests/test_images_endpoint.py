from __future__ import annotations

import io
from typing import cast

import pytest
from fastapi.datastructures import UploadFile
from starlette.datastructures import Headers

from gateway_drafts.image import ImagesService, data_uri
from gateway_drafts.schemas import ImageUploadResult
from gateway_drafts_rest.router import upload_image


def test_data_uri_builds_a_base64_data_uri() -> None:
    assert data_uri("image/png", b"ABC") == "data:image/png;base64,QUJD"


class _FakeService:
    def __init__(self) -> None:
        self.uploaded: list[str] = []

    async def upload(self, image: str) -> ImageUploadResult:
        self.uploaded.append(image)
        return ImageUploadResult(
            id=1,
            url="https://substack-post-media.s3.amazonaws.com/x.png",
            width=10,
            height=20,
            bytes=3,
            content_type="image/png",
        )


@pytest.mark.anyio
async def test_endpoint_uploads_file_as_data_uri() -> None:
    upload = UploadFile(
        file=io.BytesIO(b"ABC"),
        filename="cat.png",
        headers=Headers({"content-type": "image/png"}),
    )
    service = _FakeService()

    result = await upload_image(file=upload, service=cast(ImagesService, service))

    assert service.uploaded == ["data:image/png;base64,QUJD"]
    assert result.url == "https://substack-post-media.s3.amazonaws.com/x.png"
    assert result.width == 10
