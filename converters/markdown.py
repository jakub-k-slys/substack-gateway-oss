from __future__ import annotations

import json
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

# Draft body inline: *** before ** before * so bold+italic is matched first.
_INLINE_DRAFT = re.compile(
    r"\*\*\*(.*?)\*\*\*"  # bold + italic  (must precede **)
    r"|\*\*(.*?)\*\*"  # bold
    r"|\*(.*?)\*"  # italic
    r"|`(.*?)`"  # code
    r"|\[([^\]]+)\]\(([^)]+)\)"  # link → kept as inline text
)
_HEADING_DRAFT = re.compile(r"^(#{1,6})\s+(.*)")


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


# ------------------------------------------------------------------
# Draft body converter (ProseMirror format for Substack drafts)
# ------------------------------------------------------------------


def markdown_to_draft_body(markdown: str) -> str:
    """Convert Markdown to the JSON string expected by Substack's draft_body field.

    The output is a ProseMirror document serialised to JSON — the same format
    Substack stores internally. Unlike the note converter, this produces proper
    heading, bullet_list, and ordered_list nodes, and uses 'strong'/'em' marks.
    """
    doc = _build_draft_doc(markdown.replace("\\n", "\n"))
    return json.dumps(doc, ensure_ascii=False)


def _build_draft_doc(text: str) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    para_lines: list[str] = []
    list_type: str | None = None  # "bullet" or "ordered"
    list_items: list[list[dict[str, Any]]] = []

    def flush_para() -> None:
        nonlocal para_lines
        joined = " ".join(para_lines).strip()
        para_lines = []
        if joined:
            inline = _parse_inline_draft(joined)
            if inline:
                nodes.append(_paragraph(inline))

    def flush_list() -> None:
        nonlocal list_type, list_items
        if list_items:
            if list_type == "bullet":
                nodes.append(_draft_bullet_list(list_items))
            else:
                nodes.append(_draft_ordered_list(list_items))
        list_type = None
        list_items = []

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            flush_para()
            continue

        if m := _HEADING_DRAFT.match(line):
            flush_para()
            flush_list()
            level = len(m.group(1))
            heading_text = m.group(2).strip()
            if heading_text:
                nodes.append(_draft_heading(level, _parse_inline_draft(heading_text)))

        elif m := _UNORDERED.match(line):
            flush_para()
            if list_type != "bullet":
                flush_list()
                list_type = "bullet"
            inline = _parse_inline_draft(m.group(1).strip())
            if inline:
                list_items.append(inline)

        elif m := _ORDERED.match(line):
            flush_para()
            if list_type != "ordered":
                flush_list()
                list_type = "ordered"
            inline = _parse_inline_draft(m.group(2).strip())
            if inline:
                list_items.append(inline)

        else:
            if list_type:
                flush_list()
            para_lines.append(stripped)

    flush_para()
    flush_list()

    return {"type": "doc", "content": nodes}


def _parse_inline_draft(text: str) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    last_end = 0
    for m in _INLINE_DRAFT.finditer(text):
        if m.start() > last_end:
            nodes.append(_text_draft(text[last_end : m.start()]))
        if m.group(1) is not None:  # bold + italic
            nodes.append(_text_draft(m.group(1), "strong", "em"))
        elif m.group(2) is not None:  # bold
            nodes.append(_text_draft(m.group(2), "strong"))
        elif m.group(3) is not None:  # italic
            nodes.append(_text_draft(m.group(3), "em"))
        elif m.group(4) is not None:  # code
            nodes.append(_text_draft(m.group(4), "code"))
        else:  # link → plain inline text
            nodes.append(_text_draft(f"{m.group(5)} ({m.group(6)})"))
        last_end = m.end()
    if last_end < len(text):
        nodes.append(_text_draft(text[last_end:]))
    return [n for n in nodes if n["text"]]


def _text_draft(text: str, *mark_types: str) -> dict[str, Any]:
    node: dict[str, Any] = {"type": "text", "text": text}
    if mark_types:
        node["marks"] = [{"type": t} for t in mark_types]
    return node


def _draft_heading(level: int, content: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "heading", "attrs": {"level": level}, "content": content}


def _draft_bullet_list(items: list[list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "type": "bullet_list",
        "content": [_draft_list_item(inline) for inline in items],
    }


def _draft_ordered_list(items: list[list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "type": "ordered_list",
        "attrs": {"start": 1, "type": None, "order": 1},
        "content": [_draft_list_item(inline) for inline in items],
    }


def _draft_list_item(content: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "list_item", "content": [_paragraph(content)]}
