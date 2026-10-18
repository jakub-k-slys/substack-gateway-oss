"""Shared builders for the draft Markdown dialect tests."""

from __future__ import annotations

from typing import Any

from gateway_drafts.converters.dialect.attrs import fill_defaults


def _t(text: str, *marks: str, href: str | None = None) -> dict[str, Any]:
    """Build a ProseMirror text node; ``href`` adds a default-attrs link mark first."""
    node: dict[str, Any] = {"type": "text", "text": text}
    ms: list[dict[str, Any]] = [{"type": m} for m in marks]
    if href:
        ms.insert(
            0,
            {
                "type": "link",
                "attrs": {
                    "href": href,
                    "target": "_blank",
                    "rel": "noopener noreferrer nofollow",
                    "class": None,
                },
            },
        )
    if ms:
        node["marks"] = ms
    return node


def _p(text: str, align: str | None = None) -> dict[str, Any]:
    """Build a paragraph holding one plain text node, with ``textAlign``."""
    return {"type": "paragraph", "attrs": {"textAlign": align}, "content": [_t(text)]}


def doc_with_image(**image2_attrs: Any) -> dict[str, Any]:
    """Build a doc holding one ``captionedImage`` with these ``image2`` attrs."""
    attrs = fill_defaults("image2", {"alt": "H", **image2_attrs})
    image = {"type": "captionedImage", "content": [{"type": "image2", "attrs": attrs}]}
    return {"type": "doc", "content": [image]}
