from __future__ import annotations

import json
import re
from collections.abc import Callable
from typing import Any

_INLINE_DRAFT = re.compile(
    r"~~(.*?)~~"
    r"|\*\*\*(.*?)\*\*\*"
    r"|\*\*(.*?)\*\*"
    r"|\*(.*?)\*"
    r"|`(.*?)`"
    r"|\[([^\]]+)\]\(([^)]+)\)"
)
_HEADING_DRAFT = re.compile(r"^(#{1,6})\s+(.*)")
_UNORDERED = re.compile(r"^[-*]\s+(.*)")
_ORDERED = re.compile(r"^(\d+)\.\s+(.*)")
_FENCE_OPEN = re.compile(r"^```(\w*)\s*$")
_FENCE_CLOSE = re.compile(r"^```\s*$")
_BLOCKQUOTE_LINE = re.compile(r"^> ?(.*)", re.DOTALL)
_PULLQUOTE_LINE = re.compile(r"^\|> ?(.*)", re.DOTALL)


def markdown_to_draft_body(markdown: str) -> str:
    doc = {
        "type": "doc",
        "content": _build_nodes(markdown.replace("\\n", "\n").splitlines()),
    }
    return json.dumps(doc, ensure_ascii=False)


def _build_nodes(lines: list[str]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    para_lines: list[str] = []
    list_type: str | None = None
    list_items: list[list[dict[str, Any]]] = []
    quote_type: str | None = None
    quote_lines: list[str] = []
    in_fence = False
    fence_lang = ""
    fence_lines: list[str] = []

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

    def flush_quote() -> None:
        nonlocal quote_type, quote_lines
        if quote_lines:
            inner = _build_nodes(quote_lines)
            if inner:
                if quote_type == "blockquote":
                    nodes.append({"type": "blockquote", "content": inner})
                else:
                    nodes.append(
                        {
                            "type": "pullquote",
                            "attrs": {"align": None, "color": None},
                            "content": inner,
                        }
                    )
        quote_type = None
        quote_lines = []

    for line in lines:
        stripped = line.strip()

        if in_fence:
            if _FENCE_CLOSE.match(stripped):
                in_fence = False
                nodes.append(_draft_code_block(fence_lang, "\n".join(fence_lines)))
                fence_lang = ""
                fence_lines = []
            else:
                fence_lines.append(line)
            continue

        if match := _FENCE_OPEN.match(stripped):
            flush_para()
            flush_list()
            flush_quote()
            in_fence = True
            fence_lang = match.group(1)
            continue

        if match := _BLOCKQUOTE_LINE.match(stripped):
            flush_para()
            flush_list()
            if quote_type != "blockquote":
                flush_quote()
                quote_type = "blockquote"
            quote_lines.append(match.group(1))
            continue

        if match := _PULLQUOTE_LINE.match(stripped):
            flush_para()
            flush_list()
            if quote_type != "pullquote":
                flush_quote()
                quote_type = "pullquote"
            quote_lines.append(match.group(1))
            continue

        if not stripped:
            flush_para()
            if quote_type:
                quote_lines.append("")
            continue

        if match := _HEADING_DRAFT.match(line):
            flush_para()
            flush_list()
            flush_quote()
            level = len(match.group(1))
            heading_text = match.group(2).strip()
            if heading_text:
                nodes.append(_draft_heading(level, _parse_inline_draft(heading_text)))
            continue

        if match := _UNORDERED.match(line):
            flush_para()
            flush_quote()
            if list_type != "bullet":
                flush_list()
                list_type = "bullet"
            inline = _parse_inline_draft(match.group(1).strip())
            if inline:
                list_items.append(inline)
            continue

        if match := _ORDERED.match(line):
            flush_para()
            flush_quote()
            if list_type != "ordered":
                flush_list()
                list_type = "ordered"
            inline = _parse_inline_draft(match.group(2).strip())
            if inline:
                list_items.append(inline)
            continue

        if list_type:
            flush_list()
        if quote_type:
            flush_quote()
        para_lines.append(stripped)

    flush_para()
    flush_list()
    flush_quote()
    return nodes


def _parse_inline_generic(
    text: str,
    pattern: re.Pattern[str],
    handlers: list[Callable[[re.Match[str]], dict[str, Any] | None]],
) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    last_end = 0
    for match in pattern.finditer(text):
        if match.start() > last_end:
            nodes.append(_text_draft(text[last_end : match.start()]))
        for handler in handlers:
            node = handler(match)
            if node is not None:
                nodes.append(node)
                break
        last_end = match.end()
    if last_end < len(text):
        nodes.append(_text_draft(text[last_end:]))
    return [node for node in nodes if node.get("text")]


def _paragraph(content: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "paragraph", "content": content}


def _text_draft(text: str, *mark_types: str) -> dict[str, Any]:
    node: dict[str, Any] = {"type": "text", "text": text}
    if mark_types:
        node["marks"] = [{"type": mark_type} for mark_type in mark_types]
    return node


def _link_node(text: str, url: str) -> dict[str, Any]:
    return {
        "type": "text",
        "marks": [
            {
                "type": "link",
                "attrs": {
                    "href": url,
                    "target": "_blank",
                    "rel": "noopener noreferrer nofollow",
                    "class": None,
                },
            }
        ],
        "text": text,
    }


def _h_draft_strike(match: re.Match[str]) -> dict[str, Any] | None:
    group = match.group(1)
    return _text_draft(group, "strikethrough") if group is not None else None


def _h_draft_bold_italic(match: re.Match[str]) -> dict[str, Any] | None:
    group = match.group(2)
    return _text_draft(group, "strong", "em") if group is not None else None


def _h_draft_bold(match: re.Match[str]) -> dict[str, Any] | None:
    group = match.group(3)
    return _text_draft(group, "strong") if group is not None else None


def _h_draft_italic(match: re.Match[str]) -> dict[str, Any] | None:
    group = match.group(4)
    return _text_draft(group, "em") if group is not None else None


def _h_draft_code(match: re.Match[str]) -> dict[str, Any] | None:
    group = match.group(5)
    return _text_draft(group, "code") if group is not None else None


def _h_draft_link(match: re.Match[str]) -> dict[str, Any] | None:
    group = match.group(6)
    return _link_node(group, match.group(7)) if group is not None else None


_DRAFT_INLINE_HANDLERS: list[Callable[[re.Match[str]], dict[str, Any] | None]] = [
    _h_draft_strike,
    _h_draft_bold_italic,
    _h_draft_bold,
    _h_draft_italic,
    _h_draft_code,
    _h_draft_link,
]


def _parse_inline_draft(text: str) -> list[dict[str, Any]]:
    return _parse_inline_generic(text, _INLINE_DRAFT, _DRAFT_INLINE_HANDLERS)


def _draft_heading(level: int, content: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "heading", "attrs": {"level": level}, "content": content}


def _draft_code_block(language: str, text: str) -> dict[str, Any]:
    return {
        "type": "highlighted_code_block",
        "attrs": {"language": language or None, "nodeId": None},
        "content": [{"type": "text", "text": text}],
    }


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


def draft_body_to_markdown(body: str) -> str:
    doc = json.loads(body)
    blocks: list[str] = []
    for node in doc.get("content", []):
        block = _prosemirror_node_to_md(node)
        if block is not None:
            blocks.append(block)
    return "\n\n".join(blocks)


def _prosemirror_node_to_md(node: dict[str, Any]) -> str | None:
    node_type = node.get("type")

    if node_type == "paragraph":
        text = _inline_to_md(node.get("content", []))
        return text if text.strip() else None

    if node_type == "heading":
        level = node.get("attrs", {}).get("level", 1)
        text = _inline_to_md(node.get("content", []))
        return f"{'#' * level} {text}" if text.strip() else None

    if node_type == "highlighted_code_block":
        language = (node.get("attrs") or {}).get("language") or ""
        text = "".join(item.get("text", "") for item in node.get("content", []))
        fence = f"```{language}" if language else "```"
        return f"{fence}\n{text}\n```"

    if node_type in ("blockquote", "pullquote"):
        prefix = "> " if node_type == "blockquote" else "|> "
        blank = ">" if node_type == "blockquote" else "|>"
        inner_blocks = [_prosemirror_node_to_md(item) for item in node.get("content", [])]
        inner_md = "\n\n".join(block for block in inner_blocks if block is not None)
        return "\n".join(
            f"{prefix}{line}" if line else blank for line in inner_md.splitlines()
        )

    if node_type == "bullet_list":
        lines = [
            f"- {_inline_to_md(paragraph.get('content', []))}"
            for item in node.get("content", [])
            for paragraph in item.get("content", [])
            if _inline_to_md(paragraph.get("content", [])).strip()
        ]
        return "\n".join(lines) if lines else None

    if node_type == "ordered_list":
        lines = []
        counter = 1
        for item in node.get("content", []):
            for paragraph in item.get("content", []):
                text = _inline_to_md(paragraph.get("content", []))
                if text.strip():
                    lines.append(f"{counter}. {text}")
                    counter += 1
        return "\n".join(lines) if lines else None

    return None


def _inline_to_md(content: list[dict[str, Any]]) -> str:
    parts = []
    for node in content:
        text = node.get("text", "")
        node_marks = node.get("marks", [])
        marks = {mark["type"] for mark in node_marks}
        mark_attrs = {mark["type"]: mark.get("attrs") or {} for mark in node_marks}

        if "link" in marks:
            href = mark_attrs["link"].get("href", "")
            leading = text[: len(text) - len(text.lstrip())]
            trailing = text[len(text.rstrip()) :]
            text = f"{leading}[{text.strip()}]({href}){trailing}"
        elif marks and text.strip():
            leading = text[: len(text) - len(text.lstrip())]
            trailing = text[len(text.rstrip()) :]
            inner = text.strip()
            if "strong" in marks and "em" in marks:
                text = f"{leading}***{inner}***{trailing}"
            elif "strong" in marks:
                text = f"{leading}**{inner}**{trailing}"
            elif "em" in marks:
                text = f"{leading}*{inner}*{trailing}"
            elif "strikethrough" in marks:
                text = f"{leading}~~{inner}~~{trailing}"
            elif "code" in marks:
                text = f"{leading}`{inner}`{trailing}"
        parts.append(text)
    return "".join(parts)
