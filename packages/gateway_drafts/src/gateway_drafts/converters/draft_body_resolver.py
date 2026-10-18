from __future__ import annotations

from typing import Any

from gateway_core.client.publication import PublicationClient
from gateway_drafts.converters.dialect.attrs import fill_defaults
from gateway_drafts.converters.dialect.blocks import is_substack_hosted
from gateway_drafts.converters.dialect.errors import DraftMarkdownError
from gateway_drafts.converters.dialect.fences import normalize_datawrapper_url
from gateway_drafts.image import ImagesService
from gateway_drafts.watermark import (
    WatermarkService,
    WatermarkSpec,
    image_dimensions_from_url,
)

_PLACEHOLDER_PREFIX = "_unresolved_"


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
    # The parser already validated the URL at its line; this is the backstop
    # for a placeholder built some other way (still a DraftMarkdownError).
    resolve_url = normalize_datawrapper_url(node["attrs"]["url"])
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
    image_attrs = dict(attrs.get("image_attrs") or {})
    explicit_original = image_attrs.pop("srcNoWatermark", None)
    watermark = attrs.get("watermark")

    final: dict[str, Any] = {"alt": attrs.get("alt") or None}
    final_src = src
    upload_size: tuple[int, int] | None = None
    if not is_substack_hosted(src):
        result = await ImagesService(pub).upload(src)
        final_src = result.url
        upload_size = (result.width, result.height)
        final.update(
            width=result.width,
            height=result.height,
            bytes=result.bytes,
            type=result.content_type,
        )
    if watermark is not None:
        # The overlay always goes on the pristine image, never a prior result.
        original = explicit_original or final_src
        size = (
            upload_size
            or image_dimensions_from_url(original)
            or image_dimensions_from_url(final_src)
        )
        if size is None:
            raise DraftMarkdownError(f"cannot watermark {src}: image size unknown")
        spec = WatermarkSpec(
            scale=watermark["scale"],
            position=watermark["position"],
            opacity=watermark["opacity"],
        )
        final_src = await WatermarkService(pub).apply(original, *size, spec)
        final["srcNoWatermark"] = original
    elif explicit_original is not None:
        final["srcNoWatermark"] = explicit_original
    final.update(image_attrs)
    final["src"] = final_src
    return {
        "type": "captionedImage",
        "content": [{"type": "image2", "attrs": fill_defaults("image2", final)}],
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
