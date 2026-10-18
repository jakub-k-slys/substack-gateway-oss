"""Shared builders for the draft Markdown dialect tests."""

from __future__ import annotations

from typing import Any


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
