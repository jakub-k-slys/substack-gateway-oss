from __future__ import annotations

from typing import cast

import pytest

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


class _Resp:
    def json(self) -> dict:
        return {"url": "https://s3/wm.png"}


class _Pub:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    async def post(self, path: str, json: dict | None = None) -> _Resp:
        self.calls.append({"path": path, "json": json})
        return _Resp()


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
