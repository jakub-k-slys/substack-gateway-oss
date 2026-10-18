"""Inline Markdown <-> ProseMirror text nodes for the draft dialect.

Supported marks: ``strong`` (``**``), ``em`` (``*``), ``strikethrough`` (``~~``),
optionally inside one ``link`` (``[...](href)``), and ``code`` (`` ` ``) alone.
Delimiters nest in the fixed order link > strong > em > strikethrough and wrap
the exact text, inner whitespace included (``** x **`` is strong " x ").

``parse_inline`` is a character scanner with a mark stack: a delimiter closes
the mark on top of the stack if it can, otherwise opens a mark that is not yet
active, otherwise it is literal. Openers still unclosed at the end become
literal text, so parsing never fails. ``serialize_inline`` returns ``None``
whenever the content cannot be written so that ``parse_inline`` gives it back.
"""

from __future__ import annotations

import string
from dataclasses import dataclass
from typing import Any

from gateway_drafts.converters.dialect.attrs import diff_from_defaults, fill_defaults

_RANK = {"link": 0, "strong": 1, "em": 2, "strikethrough": 3, "code": 4}
_DELIMITER = {"strong": "**", "em": "*", "strikethrough": "~~"}
_TEXT_ESCAPED = frozenset("\\*`[]~{}")
_HREF_ESCAPED = frozenset("\\()")
_PUNCTUATION = frozenset(string.punctuation)

Node = dict[str, Any]
Mark = dict[str, Any]


def escape_text(text: str) -> str:
    """Backslash-escape every character the inline dialect gives a meaning to."""
    return "".join("\\" + c if c in _TEXT_ESCAPED else c for c in text)


def _escape_href(href: str) -> str:
    return "".join("\\" + c if c in _HREF_ESCAPED else c for c in href)


# --- parsing ----------------------------------------------------------------


@dataclass
class _Token:
    kind: str  # "text" | "code" | "open" | "close"
    value: str  # literal text, code text, or the raw delimiter
    mark: str = ""
    href: str = ""


class _Scanner:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.tokens: list[_Token] = []
        self.stack: list[int] = []  # indices of open tokens
        self.buffer: list[str] = []
        # Once a link target finds no ")" before the end, no later one can:
        # every scan starts right after "(" with the same escape alignment.
        self.no_target_close = False

    def run(self) -> list[_Token]:
        text = self.text
        while self.pos < len(text):
            char = text[self.pos]
            if char == "\\" and text[self.pos + 1 : self.pos + 2] in _PUNCTUATION:
                self._literal(text[self.pos + 1], 2)
            elif char == "`":
                self._code()
            elif char == "*" or text.startswith("~~", self.pos):
                self._delimiter()
            elif char == "[" and not self._active("link"):
                self._open("link", "[")
            elif char == "]" and self._top() == "link":
                self._close_link()
            else:
                self._literal(char, 1)
        self._flush()
        for index in self.stack:  # unclosed openers are literal text
            self.tokens[index] = _Token("text", self.tokens[index].value)
        return self.tokens

    def _top(self) -> str:
        return self.tokens[self.stack[-1]].mark if self.stack else ""

    def _active(self, mark: str) -> bool:
        return any(self.tokens[index].mark == mark for index in self.stack)

    def _literal(self, chars: str, advance: int) -> None:
        self.buffer.append(chars)
        self.pos += advance

    def _flush(self) -> None:
        if self.buffer:
            self.tokens.append(_Token("text", "".join(self.buffer)))
            self.buffer = []

    def _open(self, mark: str, raw: str) -> None:
        self._flush()
        self.stack.append(len(self.tokens))
        self.tokens.append(_Token("open", raw, mark))
        self.pos += len(raw)

    def _close(self, raw: str) -> None:
        self._flush()
        mark = self.tokens[self.stack.pop()].mark
        self.tokens.append(_Token("close", raw, mark))
        self.pos += len(raw)

    def _code(self) -> None:
        end = self.text.find("`", self.pos + 1)
        if end <= self.pos + 1:  # unclosed or empty: literal backtick
            self._literal("`", 1)
            return
        self._flush()
        self.tokens.append(_Token("code", self.text[self.pos + 1 : end]))
        self.pos = end + 1

    def _delimiter(self) -> None:
        top = self._top()
        if self.text[self.pos] == "~":
            if top == "strikethrough":
                self._close("~~")
            elif not self._active("strikethrough"):
                self._open("strikethrough", "~~")
            else:
                self._literal("~", 1)
            return
        double = self.text.startswith("**", self.pos)
        if top == "em":
            self._close("*")
        elif top == "strong" and double:
            self._close("**")
        elif double and not self._active("strong"):
            self._open("strong", "**")
        elif not self._active("em"):
            self._open("em", "*")
        else:
            self._literal("*", 1)

    def _close_link(self) -> None:
        text = self.text
        pos = self.pos + 1
        if self.no_target_close or text[pos : pos + 1] != "(":
            self._literal("]", 1)
            return
        href: list[str] = []
        pos += 1
        while pos < len(text):
            char = text[pos]
            if char == "\\" and text[pos + 1 : pos + 2] in _PUNCTUATION:
                href.append(text[pos + 1])
                pos += 2
            elif char == ")":
                opener = self.tokens[self.stack[-1]]
                opener.href = "".join(href)
                self._close(text[self.pos : pos + 1])
                return
            else:
                href.append(char)
                pos += 1
        self.no_target_close = True
        self._literal("]", 1)


def _mark_for(token: _Token) -> Mark:
    if token.mark == "link":
        return {"type": "link", "attrs": fill_defaults("link", {"href": token.href})}
    return {"type": token.mark}


def _append(nodes: list[Node], text: str, marks: list[Mark]) -> None:
    if not text:
        return
    ordered = sorted(marks, key=lambda mark: _RANK[mark["type"]])
    if nodes and nodes[-1].get("marks", []) == ordered:
        nodes[-1]["text"] += text
        return
    node: Node = {"type": "text", "text": text}
    if ordered:
        node["marks"] = ordered
    nodes.append(node)


def parse_inline(text: str) -> list[Node]:
    """Parse inline dialect Markdown into merged ProseMirror text nodes."""
    nodes: list[Node] = []
    active: list[Mark] = []
    for token in _Scanner(text).run():
        if token.kind == "text":
            _append(nodes, token.value, active)
        elif token.kind == "code":
            _append(nodes, token.value, [*active, {"type": "code"}])
        elif token.kind == "open":
            active.append(_mark_for(token))
        else:
            active.pop()
    return nodes


# --- serializing ------------------------------------------------------------


def _expressible_marks(node: Any) -> list[Mark] | None:
    """Return the node's marks in canonical order, or None if not expressible."""
    if not isinstance(node, dict) or node.get("type") != "text":
        return None
    text = node.get("text")
    marks = node.get("marks", [])
    if not isinstance(text, str) or not isinstance(marks, list):
        return None
    if not all(isinstance(m, dict) and m.get("type") in _RANK for m in marks):
        return None
    types = [mark["type"] for mark in marks]
    if len(set(types)) != len(types):
        return None
    if "code" in types and (len(types) > 1 or "`" in text):
        return None
    for mark in marks:
        if mark["type"] == "link" and not _plain_link(mark):
            return None
    return sorted(marks, key=lambda mark: _RANK[mark["type"]])


def _plain_link(mark: Mark) -> bool:
    attrs = mark.get("attrs")
    if not isinstance(attrs, dict) or not isinstance(attrs.get("href"), str):
        return False
    return set(diff_from_defaults("link", attrs)) <= {"href"}


def _opener(mark: Mark) -> str:
    return "[" if mark["type"] == "link" else _DELIMITER[mark["type"]]


def _closer(mark: Mark) -> str:
    if mark["type"] == "link":
        return "](" + _escape_href(mark["attrs"]["href"]) + ")"
    return _DELIMITER[mark["type"]]


def serialize_inline(content: list[Node]) -> str | None:
    """Write text nodes as inline dialect Markdown, or None if not expressible."""
    out: list[str] = []
    stack: list[Mark] = []
    for node in content:
        marks = _expressible_marks(node)
        if marks is None:
            return None
        is_code = bool(marks) and marks[0]["type"] == "code"
        wanted = [] if is_code else marks
        keep = 0
        while keep < min(len(stack), len(wanted)) and stack[keep] == wanted[keep]:
            keep += 1
        while len(stack) > keep:
            out.append(_closer(stack.pop()))
        for mark in wanted[keep:]:
            out.append(_opener(mark))
            stack.append(mark)
        text = node["text"]
        out.append(f"`{text}`" if is_code else escape_text(text))
    while stack:
        out.append(_closer(stack.pop()))
    markdown = "".join(out)
    return markdown if parse_inline(markdown) == content else None
