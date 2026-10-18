from __future__ import annotations

from typing import cast

import pytest

from gateway_core.client.publication import PublicationClient
from gateway_drafts.converters.dialect.errors import DraftMarkdownError
from gateway_drafts.converters.draft_body_resolver import (
    UnresolvedNodeError,
    resolve_draft_body,
)


class _FakePub:
    """Stand-in publication client; the resolver makes no calls in this PR."""


@pytest.mark.anyio
async def test_plain_doc_is_returned_unchanged() -> None:
    doc = {
        "type": "doc",
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "hi"}]}],
    }
    assert await resolve_draft_body(doc, cast(PublicationClient, _FakePub())) == doc


@pytest.mark.anyio
async def test_latex_block_is_left_untouched() -> None:
    doc = {
        "type": "doc",
        "content": [
            {
                "type": "latex_block",
                "attrs": {"persistentExpression": "x", "id": "ABCDEFGHIJ"},
            }
        ],
    }
    assert await resolve_draft_body(doc, cast(PublicationClient, _FakePub())) == doc


@pytest.mark.anyio
async def test_unresolved_placeholder_raises() -> None:
    doc = {
        "type": "doc",
        "content": [{"type": "_unresolved_video", "attrs": {"src": "https://x/y.mp4"}}],
    }
    with pytest.raises(UnresolvedNodeError):
        await resolve_draft_body(doc, cast(PublicationClient, _FakePub()))


class _FakeResp:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def json(self) -> dict:
        return self._payload


class _EmbedPub:
    """Publication client stub that answers the datawrapper-embed GET."""

    def __init__(self, payload: dict) -> None:
        self._payload = payload
        self.calls: list[dict] = []

    async def get(self, path: str, params: dict | None = None):
        self.calls.append({"path": path, "params": params})
        return _FakeResp(self._payload)


_EMBED = {
    "url": "https://datawrapper.dwcdn.net/boimj/2/",
    "thumbnail_url": "https://s3/x.png",
    "thumbnail_url_full": "https://s3/x-full.png",
    "height": 400,
    "title": "Which mistake hurts more",
    "description": "",
}


@pytest.mark.anyio
async def test_datawrapper_placeholder_is_resolved() -> None:
    doc = {
        "type": "doc",
        "content": [
            {
                "type": "_unresolved_datawrapper",
                "attrs": {"url": "https://datawrapper.dwcdn.net/boimj/2/"},
            }
        ],
    }
    pub = _EmbedPub(_EMBED)
    resolved = await resolve_draft_body(doc, cast(PublicationClient, pub))
    assert resolved["content"][0] == {
        "type": "datawrapper",
        "attrs": {
            "url": "https://datawrapper.dwcdn.net/boimj/2/",
            "thumbnail_url": "https://s3/x.png",
            "thumbnail_url_full": "https://s3/x-full.png",
            "height": 400,
            "title": "Which mistake hurts more",
            "description": "",
        },
    }
    # the embed endpoint was called with the normalized resolve URL
    assert pub.calls == [
        {
            "path": "datawrapper-embed",
            "params": {"url": "https://www.datawrapper.de/_/boimj/"},
        }
    ]


class _ImagePub:
    """Publication client stub that answers the image upload POST."""

    def __init__(self, payload: dict) -> None:
        self._payload = payload
        self.calls: list[dict] = []

    async def post(self, path: str, json: dict | None = None):
        self.calls.append({"path": path, "json": json})
        return _FakeResp(self._payload)


_IMAGE_RESP = {
    "id": 1,
    "url": "https://substack-post-media.s3.amazonaws.com/x.png",
    "contentType": "image/png",
    "bytes": 72180,
    "imageWidth": 2387,
    "imageHeight": 203,
}


@pytest.mark.anyio
async def test_image_placeholder_is_resolved() -> None:
    doc = {
        "type": "doc",
        "content": [
            {
                "type": "_unresolved_image",
                "attrs": {"src": "data:image/png;base64,QUJD", "alt": "A cat"},
            }
        ],
    }
    pub = _ImagePub(_IMAGE_RESP)
    resolved = await resolve_draft_body(doc, cast(PublicationClient, pub))

    node = resolved["content"][0]
    assert node["type"] == "captionedImage"
    image = node["content"][0]
    assert image["type"] == "image2"
    assert image["attrs"]["src"] == "https://substack-post-media.s3.amazonaws.com/x.png"
    assert image["attrs"]["width"] == 2387
    assert image["attrs"]["height"] == 203
    assert image["attrs"]["bytes"] == 72180
    assert image["attrs"]["type"] == "image/png"
    assert image["attrs"]["alt"] == "A cat"
    assert image["attrs"]["isProcessing"] is False
    assert pub.calls == [
        {"path": "image", "json": {"image": "data:image/png;base64,QUJD"}}
    ]


@pytest.mark.anyio
async def test_image_empty_alt_becomes_null() -> None:
    doc = {
        "type": "doc",
        "content": [
            {
                "type": "_unresolved_image",
                "attrs": {"src": "https://x/y.png", "alt": ""},
            }
        ],
    }
    resolved = await resolve_draft_body(
        doc, cast(PublicationClient, _ImagePub(_IMAGE_RESP))
    )
    assert resolved["content"][0]["content"][0]["attrs"]["alt"] is None


@pytest.mark.anyio
@pytest.mark.parametrize(
    "src",
    [
        "https://substack-post-media.s3.amazonaws.com/public/images/x.png",
        "https://substackcdn.com/image/fetch/x.png",
    ],
)
async def test_substack_hosted_image_is_not_reuploaded(src: str) -> None:
    doc = {
        "type": "doc",
        "content": [
            {"type": "_unresolved_image", "attrs": {"src": src, "alt": "A cat"}}
        ],
    }
    pub = _ImagePub(_IMAGE_RESP)
    resolved = await resolve_draft_body(doc, cast(PublicationClient, pub))

    image = resolved["content"][0]["content"][0]
    assert image["type"] == "image2"
    # URL used verbatim; no re-upload, so no upload metadata is invented.
    assert image["attrs"]["src"] == src
    assert image["attrs"]["alt"] == "A cat"
    assert image["attrs"]["width"] is None
    assert image["attrs"]["height"] is None
    assert image["attrs"]["bytes"] is None
    assert image["attrs"]["type"] is None
    assert image["attrs"]["isProcessing"] is False
    # crucially: the image endpoint was never called
    assert pub.calls == []


class _WatermarkPub:
    """Publication client stub answering both image upload and watermark POSTs."""

    def __init__(self) -> None:
        self.calls: list[dict] = []

    async def post(self, path: str, json: dict | None = None):
        self.calls.append({"path": path, "json": json})
        if path == "image/watermark":
            return _FakeResp(
                {"url": "https://substack-post-media.s3.amazonaws.com/wm.png"}
            )
        return _FakeResp(_IMAGE_RESP)


_HOSTED = "https://substack-post-media.s3.amazonaws.com/public/images/x_1536x1024.png"
_WM = {"scale": 0.06, "position": "top-right", "opacity": 65}


def _image_doc(src: str, *, image_attrs: dict | None = None, watermark=None) -> dict:
    return {
        "type": "doc",
        "content": [
            {
                "type": "_unresolved_image",
                "attrs": {
                    "src": src,
                    "alt": "A cat",
                    "image_attrs": image_attrs or {},
                    "watermark": watermark,
                },
            }
        ],
    }


@pytest.mark.anyio
async def test_resolver_watermarks_hosted_image() -> None:
    pub = _WatermarkPub()
    resolved = await resolve_draft_body(
        _image_doc(_HOSTED, watermark=_WM), cast(PublicationClient, pub)
    )
    attrs = resolved["content"][0]["content"][0]["attrs"]
    assert attrs["src"] == "https://substack-post-media.s3.amazonaws.com/wm.png"
    assert attrs["srcNoWatermark"] == _HOSTED
    assert attrs["alt"] == "A cat"
    assert attrs["isProcessing"] is False
    assert pub.calls == [
        {
            "path": "image/watermark",
            "json": {
                "image": _HOSTED,
                "offsetX": 1433,
                "offsetY": 6,
                "width": 93,
                "height": 93,
                "opacity": 65,
            },
        }
    ]


@pytest.mark.anyio
async def test_resolver_watermarks_the_upload_of_an_external_image() -> None:
    pub = _WatermarkPub()
    resolved = await resolve_draft_body(
        _image_doc(
            "https://example.com/cat.png",
            watermark={"scale": 0.1, "position": "bottom-left", "opacity": 30},
        ),
        cast(PublicationClient, pub),
    )
    attrs = resolved["content"][0]["content"][0]["attrs"]
    uploaded = _IMAGE_RESP["url"]
    assert attrs["src"] == "https://substack-post-media.s3.amazonaws.com/wm.png"
    assert attrs["srcNoWatermark"] == uploaded
    assert (attrs["width"], attrs["height"], attrs["bytes"]) == (2387, 203, 72180)
    assert attrs["type"] == "image/png"
    # dimensions come from the upload result: 2387 wide, 203 tall. 10 % of the
    # width (239) is taller than the image, so the square is clamped to the
    # height (203) and the bottom offset to 0 instead of going negative.
    size, offset = 203, 10
    assert pub.calls == [
        {"path": "image", "json": {"image": "https://example.com/cat.png"}},
        {
            "path": "image/watermark",
            "json": {
                "image": uploaded,
                "offsetX": offset + 4,
                "offsetY": 0,
                "width": size,
                "height": size,
                "opacity": 30,
            },
        },
    ]


@pytest.mark.anyio
async def test_resolver_regenerates_watermark_from_the_original() -> None:
    original = (
        "https://substack-post-media.s3.amazonaws.com/public/images/o_1000x500.png"
    )
    stale = "https://substack-post-media.s3.amazonaws.com/public/images/stale.png"
    pub = _WatermarkPub()
    resolved = await resolve_draft_body(
        _image_doc(
            stale,
            image_attrs={"srcNoWatermark": original, "imageSize": "large"},
            watermark={"scale": 0.06, "position": "top-left", "opacity": 65},
        ),
        cast(PublicationClient, pub),
    )
    attrs = resolved["content"][0]["content"][0]["attrs"]
    assert attrs["srcNoWatermark"] == original
    assert attrs["src"] == "https://substack-post-media.s3.amazonaws.com/wm.png"
    assert attrs["imageSize"] == "large"
    assert pub.calls == [
        {
            "path": "image/watermark",
            "json": {
                "image": original,
                "offsetX": 8,
                "offsetY": 4,
                "width": 60,
                "height": 60,
                "opacity": 65,
            },
        }
    ]


@pytest.mark.anyio
async def test_external_image_keeps_size_attributes() -> None:
    pub = _WatermarkPub()
    resolved = await resolve_draft_body(
        _image_doc(
            "https://example.com/cat.png",
            image_attrs={
                "imageSize": "large",
                "resizeWidth": 1200,
                "align": "center",
                "fullscreen": False,
            },
        ),
        cast(PublicationClient, pub),
    )
    attrs = resolved["content"][0]["content"][0]["attrs"]
    assert attrs["imageSize"] == "large"
    assert attrs["resizeWidth"] == 1200
    assert attrs["align"] == "center"
    assert attrs["fullscreen"] is False
    assert attrs["srcNoWatermark"] is None
    assert attrs["width"] == 2387
    assert [c["path"] for c in pub.calls] == ["image"]


@pytest.mark.anyio
async def test_unknown_size_raises_before_watermark_call() -> None:
    src = "https://substackcdn.com/image/fetch/abc"
    pub = _WatermarkPub()
    with pytest.raises(DraftMarkdownError) as excinfo:
        await resolve_draft_body(
            _image_doc(src, watermark=_WM), cast(PublicationClient, pub)
        )
    assert excinfo.value.message == f"cannot watermark {src}: image size unknown"
    assert excinfo.value.line is None
    assert pub.calls == []


@pytest.mark.anyio
async def test_bad_datawrapper_placeholder_is_a_markdown_error() -> None:
    # Backstop: a placeholder that bypassed the parser still fails as a
    # DraftMarkdownError (REST 400 / MCP tool error), never a 500.
    doc = {
        "type": "doc",
        "content": [
            {
                "type": "_unresolved_datawrapper",
                "attrs": {"url": "https://app.datawrapper.de/chart/AbC12/visualize"},
            }
        ],
    }
    pub = _EmbedPub(_EMBED)
    with pytest.raises(DraftMarkdownError):
        await resolve_draft_body(doc, cast(PublicationClient, pub))
    assert pub.calls == []
