from __future__ import annotations

import re
from typing import Any

# Substack note payload envelope constants
_TAB_ID = "for-you"
_SURFACE = "feed"
_REPLY_MIN_ROLE = "everyone"
_DOC_TYPE = "doc"
_SCHEMA_VERSION = "v1"

# Inline formatting: bold before italic so ** is not consumed by single-* rule.
_INLINE = re.compile(
    r"\*\*(.*?)\*\*"  # bold
    r"|\*(.*?)\*"  # italic
    r"|`(.*?)`"  # code
    r"|\[([^\]]+)\]\(([^)]+)\)"  # link → "text (url)"
)
_HEADING = re.compile(r"^#{1,6}\s+(.*)")
_UNORDERED = re.compile(r"^[-*]\s+(.*)")
_ORDERED = re.compile(r"^(\d+)\.\s+(.*)")


def markdown_to_doc(markdown: str) -> dict[str, Any]:
    """Parse a markdown string into a Substack ProseMirror document node.

    Raises ValueError if the markdown is empty or produces no content.
    """
    text = markdown.replace("\\n", "\n")

    if not text.strip():
        raise ValueError(
            "Note body cannot be empty"
            " - at least one paragraph with content is required"
        )

    paragraphs: list[dict[str, Any]] = []
    for block in re.split(r"\n\n", text):
        paragraphs.extend(_process_block(block))

    if not paragraphs:
        raise ValueError("Note must contain at least one paragraph with actual content")

    return {
        "type": _DOC_TYPE,
        "attrs": {"schemaVersion": _SCHEMA_VERSION},
        "content": paragraphs,
    }


def markdown_to_note_payload(
    markdown: str, attachment_ids: list[str] | None = None
) -> dict[str, Any]:
    """Convert a markdown string to a Substack note creation payload."""
    payload: dict[str, Any] = {
        "bodyJson": markdown_to_doc(markdown),
        "tabId": _TAB_ID,
        "surface": _SURFACE,
        "replyMinimumRole": _REPLY_MIN_ROLE,
    }

    if attachment_ids:
        payload["attachmentIds"] = attachment_ids

    return payload


def _process_block(block: str) -> list[dict[str, Any]]:
    paragraphs: list[dict[str, Any]] = []
    accumulated: list[str] = []

    for line in block.split("\n"):
        if m := _HEADING.match(line):
            _flush(accumulated, paragraphs)
            accumulated.clear()
            text = m.group(1).rstrip()
            if text:
                paragraphs.append(_paragraph([_bold(n) for n in _parse_inline(text)]))

        elif m := _UNORDERED.match(line):
            _flush(accumulated, paragraphs)
            accumulated.clear()
            text = m.group(1).rstrip()
            if text:
                paragraphs.append(_paragraph([_text("• ")] + _parse_inline(text)))

        elif m := _ORDERED.match(line):
            _flush(accumulated, paragraphs)
            accumulated.clear()
            text = m.group(2).rstrip()
            if text:
                paragraphs.append(
                    _paragraph([_text(f"{m.group(1)}. ")] + _parse_inline(text))
                )

        elif not line.strip():
            _flush(accumulated, paragraphs)
            accumulated.clear()

        else:
            accumulated.append(line)

    _flush(accumulated, paragraphs)
    return paragraphs


def _flush(accumulated: list[str], paragraphs: list[dict[str, Any]]) -> None:
    if not accumulated:
        return
    nodes = _parse_inline("\n".join(accumulated))
    if nodes:
        paragraphs.append(_paragraph(nodes))


def _parse_inline(text: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    last_end = 0
    for m in _INLINE.finditer(text):
        if m.start() > last_end:
            nodes.append(_text(text[last_end : m.start()]))
        if m.group(1) is not None:
            nodes.append(_text(m.group(1), "bold"))
        elif m.group(2) is not None:
            nodes.append(_text(m.group(2), "italic"))
        elif m.group(3) is not None:
            nodes.append(_text(m.group(3), "code"))
        else:
            nodes.append(_text(f"{m.group(4)} ({m.group(5)})"))
        last_end = m.end()
    if last_end < len(text):
        nodes.append(_text(text[last_end:]))
    return [n for n in nodes if n["text"]]


def _text(text: str, mark: str | None = None) -> dict[str, Any]:
    node: dict[str, Any] = {"type": "text", "text": text}
    if mark:
        node["marks"] = [{"type": mark}]
    return node


def _bold(node: dict[str, Any]) -> dict[str, Any]:
    existing = node.get("marks", [])
    if any(m["type"] == "bold" for m in existing):
        return node
    return {**node, "marks": [*existing, {"type": "bold"}]}


def _paragraph(content: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "paragraph", "content": content}
