from __future__ import annotations

from typing import cast

import pytest

from gateway_core.client.exceptions import SubstackAPIError
from gateway_core.client.publication import PublicationClient
from gateway_drafts.watermark import (
    WatermarkService,
    WatermarkSpec,
    compute_geometry,
    image_dimensions_from_url,
)


@pytest.mark.parametrize(
    "w, h, expected", [(1536, 1024, (1433, 6, 93)), (1081, 222, (1008, 4, 65))]
)
def test_default_geometry_matches_web_editor(
    w: int, h: int, expected: tuple[int, int, int]
) -> None:
    assert compute_geometry(w, h, WatermarkSpec()) == expected


def test_other_corners_mirror() -> None:
    assert compute_geometry(1000, 500, WatermarkSpec(position="bottom-left")) == (
        8,
        500 - 60 - 4,
        60,
    )
    assert compute_geometry(1000, 500, WatermarkSpec(position="top-left")) == (8, 4, 60)
    assert compute_geometry(1000, 500, WatermarkSpec(position="bottom-right")) == (
        1000 - 60 - 8,
        500 - 60 - 4,
        60,
    )
    assert compute_geometry(1000, 500, WatermarkSpec(position="top-right")) == (
        1000 - 60 - 8,
        4,
        60,
    )


def test_scale_changes_size() -> None:
    assert compute_geometry(1000, 500, WatermarkSpec(scale=0.1)) == (892, 4, 100)


def test_dimensions_from_url() -> None:
    assert image_dimensions_from_url(
        "https://substack-post-media.s3.amazonaws.com/public/images/x_1081x222.png"
    ) == (1081, 222)
    assert image_dimensions_from_url("https://substackcdn.com/image/fetch/abc") is None


def test_dimensions_from_url_ignores_query_string() -> None:
    assert image_dimensions_from_url("https://h/public/images/x_10x20.jpeg?v=1") == (
        10,
        20,
    )


@pytest.mark.parametrize(
    "position", ["top-right", "top-left", "bottom-right", "bottom-left"]
)
def test_full_width_watermark_is_clamped_inside_the_image(position) -> None:
    # watermark=100% on a landscape image: the square cannot exceed the
    # shorter side and must stay inside the image (no negative offsets).
    x, y, size = compute_geometry(
        1000, 500, WatermarkSpec(scale=1.0, position=position)
    )
    assert size == 500
    assert 0 <= x <= 1000 - size
    assert 0 <= y <= 500 - size


@pytest.mark.parametrize(
    "position", ["top-right", "top-left", "bottom-right", "bottom-left"]
)
@pytest.mark.parametrize("scale", [0.06, 1.0])
def test_tiny_image_geometry_stays_inside(position, scale) -> None:
    x, y, size = compute_geometry(10, 10, WatermarkSpec(scale=scale, position=position))
    assert 1 <= size <= 10
    assert 0 <= x <= 10 - size
    assert 0 <= y <= 10 - size


def test_watermark_size_is_at_least_one_pixel() -> None:
    assert compute_geometry(10, 10, WatermarkSpec(scale=0.0001))[2] == 1


class _Resp:
    def __init__(self, payload: object = None, error: Exception | None = None):
        self._payload = {"url": "https://s3/wm.png"} if payload is None else payload
        self._error = error
        self.status_code = 200

    def json(self) -> object:
        if self._error is not None:
            raise self._error
        return self._payload


class _Pub:
    def __init__(self, response: _Resp | None = None) -> None:
        self.calls: list[dict] = []
        self._response = response or _Resp()

    async def post(self, path: str, json: dict | None = None) -> _Resp:
        self.calls.append({"path": path, "json": json})
        return self._response


@pytest.mark.anyio
@pytest.mark.parametrize(
    "response",
    [
        _Resp(error=ValueError("Expecting value: line 1 column 1 (char 0)")),
        _Resp(payload={}),
        _Resp(payload={"url": ""}),
        _Resp(payload={"url": 7}),
        _Resp(payload=["https://s3/wm.png"]),
    ],
)
async def test_bad_watermark_response_is_a_substack_api_error(response) -> None:
    pub = _Pub(response)
    with pytest.raises(SubstackAPIError) as exc:
        await WatermarkService(cast(PublicationClient, pub)).apply(
            "https://s3/x_1536x1024.png", 1536, 1024, WatermarkSpec()
        )
    assert exc.value.status_code == 502
    assert "https://s3/x_1536x1024.png" in exc.value.message


@pytest.mark.anyio
async def test_apply_posts_geometry_and_returns_url() -> None:
    pub = _Pub()
    url = await WatermarkService(cast(PublicationClient, pub)).apply(
        "https://s3/x_1536x1024.png", 1536, 1024, WatermarkSpec(opacity=40)
    )
    assert url == "https://s3/wm.png"
    assert pub.calls == [
        {
            "path": "image/watermark",
            "json": {
                "image": "https://s3/x_1536x1024.png",
                "offsetX": 1433,
                "offsetY": 6,
                "width": 93,
                "height": 93,
                "opacity": 40,
            },
        }
    ]
