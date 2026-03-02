from __future__ import annotations

import json
import re
from collections.abc import Callable
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

# Draft body inline: ~~ before *** before ** before * so they don't shadow each other.
# Groups: 1=strikethrough 2=bold+italic 3=bold 4=italic 5=code 6=link-text 7=link-url
_INLINE_DRAFT = re.compile(
    r"~~(.*?)~~"  # strikethrough  (must precede *)
    r"|\*\*\*(.*?)\*\*\*"  # bold + italic  (must precede **)
    r"|\*\*(.*?)\*\*"  # bold
    r"|\*(.*?)\*"  # italic
    r"|`(.*?)`"  # code
    r"|\[([^\]]+)\]\(([^)]+)\)"  # link [text](url)
)
_HEADING_DRAFT = re.compile(r"^(#{1,6})\s+(.*)")
_FENCE_OPEN = re.compile(r"^```(\w*)\s*$")
_FENCE_CLOSE = re.compile(r"^```\s*$")
_BLOCKQUOTE_LINE = re.compile(r"^> ?(.*)", re.DOTALL)
_PULLQUOTE_LINE = re.compile(r"^\|> ?(.*)", re.DOTALL)


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
                paragraphs.append(_paragraph([_text_draft("• ")] + _parse_inline(text)))

        elif m := _ORDERED.match(line):
            _flush(accumulated, paragraphs)
            accumulated.clear()
            text = m.group(2).rstrip()
            if text:
                paragraphs.append(
                    _paragraph([_text_draft(f"{m.group(1)}. ")] + _parse_inline(text))
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


def _parse_inline_generic(
    text: str,
    pattern: re.Pattern[str],
    handlers: list[Callable[[re.Match[str]], dict[str, Any] | None]],
) -> list[dict[str, Any]]:
    """Shared tokeniser for both note-body and draft-body inline markdown."""
    nodes: list[dict[str, Any]] = []
    last_end = 0
    for m in pattern.finditer(text):
        if m.start() > last_end:
            nodes.append(_text_draft(text[last_end : m.start()]))
        for handler in handlers:
            node = handler(m)
            if node is not None:
                nodes.append(node)
                break
        last_end = m.end()
    if last_end < len(text):
        nodes.append(_text_draft(text[last_end:]))
    return [n for n in nodes if n.get("text")]


# Note-body inline handlers — groups for _INLINE: 1=bold 2=italic 3=code 4/5=link
def _h_note_bold(m: re.Match[str]) -> dict[str, Any] | None:
    g = m.group(1)
    return _text_draft(g, "bold") if g is not None else None


def _h_note_italic(m: re.Match[str]) -> dict[str, Any] | None:
    g = m.group(2)
    return _text_draft(g, "italic") if g is not None else None


def _h_note_code(m: re.Match[str]) -> dict[str, Any] | None:
    g = m.group(3)
    return _text_draft(g, "code") if g is not None else None


def _h_note_link(m: re.Match[str]) -> dict[str, Any] | None:
    g = m.group(4)
    return _text_draft(f"{g} ({m.group(5)})") if g is not None else None


_NOTE_INLINE_HANDLERS: list[Callable[[re.Match[str]], dict[str, Any] | None]] = [
    _h_note_bold,
    _h_note_italic,
    _h_note_code,
    _h_note_link,
]


def _parse_inline(text: str) -> list[dict[str, Any]]:
    return _parse_inline_generic(text, _INLINE, _NOTE_INLINE_HANDLERS)


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

    Supported block elements: headings (#–######), fenced code blocks (```lang),
    blockquotes (> ), pull quotes (|> ), bullet lists (- ), ordered lists (1. ).
    Supported inline marks: **bold**, *italic*, ***bold+italic***, `code`,
    ~~strikethrough~~, [link](url).
    """
    doc = {
        "type": "doc",
        "content": _build_nodes(markdown.replace("\\n", "\n").splitlines()),
    }
    return json.dumps(doc, ensure_ascii=False)


def _build_nodes(lines: list[str]) -> list[dict[str, Any]]:
    """Recursively convert a list of markdown lines to ProseMirror content nodes.

    Called for the document root and again for the inner content of blockquotes
    and pull quotes (after stripping the > / |> prefix).
    """
    nodes: list[dict[str, Any]] = []
    para_lines: list[str] = []
    list_type: str | None = None  # "bullet" or "ordered"
    list_items: list[list[dict[str, Any]]] = []
    quote_type: str | None = None  # "blockquote" or "pullquote"
    quote_lines: list[str] = []
    in_fence: bool = False
    fence_lang: str = ""
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

        # ── Inside a fenced code block ──────────────────────────────
        if in_fence:
            if _FENCE_CLOSE.match(stripped):
                in_fence = False
                nodes.append(_draft_code_block(fence_lang, "\n".join(fence_lines)))
                fence_lang = ""
                fence_lines = []
            else:
                fence_lines.append(line)  # preserve indentation
            continue

        # ── Opening fence: ```lang ──────────────────────────────────
        if m := _FENCE_OPEN.match(stripped):
            flush_para()
            flush_list()
            flush_quote()
            in_fence = True
            fence_lang = m.group(1)
            continue

        # ── Blockquote line: > text ─────────────────────────────────
        if m := _BLOCKQUOTE_LINE.match(stripped):
            flush_para()
            flush_list()
            if quote_type != "blockquote":
                flush_quote()
                quote_type = "blockquote"
            quote_lines.append(m.group(1))
            continue

        # ── Pull-quote line: |> text ────────────────────────────────
        if m := _PULLQUOTE_LINE.match(stripped):
            flush_para()
            flush_list()
            if quote_type != "pullquote":
                flush_quote()
                quote_type = "pullquote"
            quote_lines.append(m.group(1))
            continue

        # ── Blank line ──────────────────────────────────────────────
        if not stripped:
            flush_para()
            if quote_type:
                # Propagate blank line into the quote so inner paragraphs stay separate.
                quote_lines.append("")
            continue

        # ── Heading: # … ###### ─────────────────────────────────────
        if m := _HEADING_DRAFT.match(line):
            flush_para()
            flush_list()
            flush_quote()
            level = len(m.group(1))
            heading_text = m.group(2).strip()
            if heading_text:
                nodes.append(_draft_heading(level, _parse_inline_draft(heading_text)))
            continue

        # ── Unordered list item ─────────────────────────────────────
        if m := _UNORDERED.match(line):
            flush_para()
            flush_quote()
            if list_type != "bullet":
                flush_list()
                list_type = "bullet"
            inline = _parse_inline_draft(m.group(1).strip())
            if inline:
                list_items.append(inline)
            continue

        # ── Ordered list item ───────────────────────────────────────
        if m := _ORDERED.match(line):
            flush_para()
            flush_quote()
            if list_type != "ordered":
                flush_list()
                list_type = "ordered"
            inline = _parse_inline_draft(m.group(2).strip())
            if inline:
                list_items.append(inline)
            continue

        # ── Regular paragraph text ──────────────────────────────────
        if list_type:
            flush_list()
        if quote_type:
            flush_quote()
        para_lines.append(stripped)

    flush_para()
    flush_list()
    flush_quote()
    return nodes


def _text_draft(text: str, *mark_types: str) -> dict[str, Any]:
    node: dict[str, Any] = {"type": "text", "text": text}
    if mark_types:
        node["marks"] = [{"type": t} for t in mark_types]
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


# Draft-body inline handlers — groups for _INLINE_DRAFT:
# 1=strikethrough 2=bold+italic 3=bold 4=italic 5=code 6/7=link
def _h_draft_strike(m: re.Match[str]) -> dict[str, Any] | None:
    g = m.group(1)
    return _text_draft(g, "strikethrough") if g is not None else None


def _h_draft_bold_italic(m: re.Match[str]) -> dict[str, Any] | None:
    g = m.group(2)
    return _text_draft(g, "strong", "em") if g is not None else None


def _h_draft_bold(m: re.Match[str]) -> dict[str, Any] | None:
    g = m.group(3)
    return _text_draft(g, "strong") if g is not None else None


def _h_draft_italic(m: re.Match[str]) -> dict[str, Any] | None:
    g = m.group(4)
    return _text_draft(g, "em") if g is not None else None


def _h_draft_code(m: re.Match[str]) -> dict[str, Any] | None:
    g = m.group(5)
    return _text_draft(g, "code") if g is not None else None


def _h_draft_link(m: re.Match[str]) -> dict[str, Any] | None:
    g = m.group(6)
    return _link_node(g, m.group(7)) if g is not None else None


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


# ------------------------------------------------------------------
# Draft body → Markdown (reverse converter)
# ------------------------------------------------------------------


def draft_body_to_markdown(body: str) -> str:
    """Convert a Substack draft_body JSON string back to Markdown.

    Reverses markdown_to_draft_body: heading nodes become # prefixes,
    bullet_list/ordered_list become - / N. lines, and strong/em marks
    become **/***/*** delimiters.
    """
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
        text = "".join(n.get("text", "") for n in node.get("content", []))
        fence = f"```{language}" if language else "```"
        return f"{fence}\n{text}\n```"

    if node_type in ("blockquote", "pullquote"):
        prefix = "> " if node_type == "blockquote" else "|> "
        blank = ">" if node_type == "blockquote" else "|>"
        inner_blocks = [_prosemirror_node_to_md(n) for n in node.get("content", [])]
        inner_md = "\n\n".join(b for b in inner_blocks if b is not None)
        return "\n".join(
            f"{prefix}{line}" if line else blank for line in inner_md.splitlines()
        )

    if node_type == "bullet_list":
        lines = [
            f"- {_inline_to_md(para.get('content', []))}"
            for item in node.get("content", [])
            for para in item.get("content", [])
            if _inline_to_md(para.get("content", [])).strip()
        ]
        return "\n".join(lines) if lines else None

    if node_type == "ordered_list":
        lines = []
        counter = 1
        for item in node.get("content", []):
            for para in item.get("content", []):
                text = _inline_to_md(para.get("content", []))
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
        marks = {m["type"] for m in node_marks}
        mark_attrs = {m["type"]: m.get("attrs") or {} for m in node_marks}

        if "link" in marks:
            href = mark_attrs["link"].get("href", "")
            leading = text[: len(text) - len(text.lstrip())]
            trailing = text[len(text.rstrip()) :]
            text = f"{leading}[{text.strip()}]({href}){trailing}"
        elif marks and text.strip():
            # Keep leading/trailing whitespace outside the delimiters so that
            # adjacent marks don't bleed into each other.
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
