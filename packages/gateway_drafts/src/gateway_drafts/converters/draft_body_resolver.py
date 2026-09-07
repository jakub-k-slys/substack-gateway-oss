from __future__ import annotations

import re
from typing import Any

from gateway_core.client.publication import PublicationClient
from gateway_drafts.image import ImagesService

_PLACEHOLDER_PREFIX = "_unresolved_"

_DATAWRAPPER_ID = re.compile(
    r"datawrapper\.de/_/([A-Za-z0-9]+)|dwcdn\.net/([A-Za-z0-9]+)"
)

# Images already re-hosted on Substack's own S3/CDN (e.g. uploaded earlier via
# the upload_image primitive). Re-posting a Substack-owned URL to the image
# endpoint returns a payload without the ``bytes`` field and keeps the same
# asset, so we build the node directly instead of re-uploading.
_SUBSTACK_HOSTED = re.compile(
    r"https?://[^/]*(?:substack-post-media\.s3|substackcdn\.com)", re.IGNORECASE
)


def _is_substack_hosted(src: str) -> bool:
    return _SUBSTACK_HOSTED.match(src) is not None


def _normalize_datawrapper_url(url: str) -> str:
    match = _DATAWRAPPER_ID.search(url)
    if match is None:
        raise ValueError(f"Not a Datawrapper chart URL: {url!r}")
    chart_id = match.group(1) or match.group(2)
    return f"https://www.datawrapper.de/_/{chart_id}/"


class UnresolvedNodeError(RuntimeError):
    """A placeholder node reached the resolver without a resolution branch.

    Phase-1 parsing emits ``_unresolved_*`` nodes for media that needs an HTTP
    call (images, Datawrapper). The resolver must replace every one before the
    doc is sent to Substack; a leftover placeholder is a bug, never shipped.
    """


async def resolve_draft_body(
    doc: dict[str, Any], pub: PublicationClient
) -> dict[str, Any]:
    """Walk the doc, replacing media placeholders with resolved nodes. Any
    ``_unresolved_*`` node left without a resolution branch trips the guard."""
    resolved = await _resolve_node(doc, pub)
    _assert_no_placeholders(resolved)
    return resolved


async def _resolve_node(node: Any, pub: PublicationClient) -> Any:
    if isinstance(node, dict):
        if node.get("type") == "_unresolved_datawrapper":
            return await _resolve_datawrapper(node, pub)
        if node.get("type") == "_unresolved_image":
            return await _resolve_image(node, pub)
        return {key: await _resolve_node(value, pub) for key, value in node.items()}
    if isinstance(node, list):
        return [await _resolve_node(item, pub) for item in node]
    return node


async def _resolve_datawrapper(
    node: dict[str, Any], pub: PublicationClient
) -> dict[str, Any]:
    resolve_url = _normalize_datawrapper_url(node["attrs"]["url"])
    response = await pub.get("datawrapper-embed", params={"url": resolve_url})
    data = response.json()
    return {
        "type": "datawrapper",
        "attrs": {
            "url": data["url"],
            "thumbnail_url": data.get("thumbnail_url"),
            "thumbnail_url_full": data.get("thumbnail_url_full"),
            "height": data.get("height", 400),
            "title": data.get("title", ""),
            "description": data.get("description", ""),
        },
    }


async def _resolve_image(
    node: dict[str, Any], pub: PublicationClient
) -> dict[str, Any]:
    attrs = node["attrs"]
    src = attrs["src"]
    alt = attrs.get("alt") or None
    if _is_substack_hosted(src):
        # Already on Substack's S3/CDN — use the URL as-is, no re-upload.
        return _captioned_image(src, alt)
    result = await ImagesService(pub).upload(src)
    return _captioned_image(
        result.url,
        alt,
        width=result.width,
        height=result.height,
        bytes_=result.bytes,
        content_type=result.content_type,
    )


def _captioned_image(
    src: str,
    alt: str | None,
    *,
    width: int | None = None,
    height: int | None = None,
    bytes_: int | None = None,
    content_type: str | None = None,
) -> dict[str, Any]:
    return {
        "type": "captionedImage",
        "content": [
            {
                "type": "image2",
                "attrs": {
                    "src": src,
                    "srcNoWatermark": None,
                    "fullscreen": None,
                    "imageSize": None,
                    "height": height,
                    "width": width,
                    "resizeWidth": None,
                    "bytes": bytes_,
                    "alt": alt,
                    "title": None,
                    "type": content_type,
                    "href": None,
                    "belowTheFold": False,
                    "topImage": False,
                    "internalRedirect": None,
                    "isProcessing": False,
                    "align": None,
                    "offset": False,
                },
            }
        ],
    }


def _assert_no_placeholders(node: Any) -> None:
    if isinstance(node, dict):
        node_type = node.get("type")
        if isinstance(node_type, str) and node_type.startswith(_PLACEHOLDER_PREFIX):
            raise UnresolvedNodeError(node_type)
        for value in node.values():
            _assert_no_placeholders(value)
    elif isinstance(node, list):
        for item in node:
            _assert_no_placeholders(item)
