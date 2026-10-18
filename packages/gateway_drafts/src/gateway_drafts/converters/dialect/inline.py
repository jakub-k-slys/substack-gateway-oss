"""Inline Markdown <-> ProseMirror text nodes for the draft dialect.

Supported marks: ``strong`` (``**``), ``em`` (``*``), ``strikethrough`` (``~~``),
optionally inside one ``link`` (``[...](href)``), and ``code`` (`` ` ``) alone.
Delimiters wrap the exact text, inner whitespace included (``a** x **b`` is
strong " x "), but a delimiter run with whitespace or a text boundary on both
sides is literal (``2 * 3``).

``parse_inline`` is a character scanner with a mark stack: a delimiter closes
the mark on top of the stack if it can, otherwise opens a mark that is not yet
active, otherwise it is literal. A ``]`` without a valid ``(target)`` turns its
``[`` into literal text. Openers still unclosed at the end become literal text,
so parsing never fails. ``serialize_inline`` writes the fixed nesting order
link > strong > em > strikethrough and returns ``None`` whenever the content
cannot be written so that ``parse_inline`` gives it back.
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


def _unescape(raw: str) -> str:
    out: list[str] = []
    pos = 0
    while pos < len(raw):
        if raw[pos] == "\\" and raw[pos + 1 : pos + 2] in _PUNCTUATION:
            out.append(raw[pos + 1])
            pos += 2
        else:
            out.append(raw[pos])
            pos += 1
    return "".join(out)


def _link_targets(text: str) -> dict[int, int]:
    """Map each unescaped ``(`` to its balanced ``)`` if no whitespace lies between.

    Every target scan starts right after the ``(`` of a ``](``, which always
    begins a fresh escape pair, so one left-to-right pass serves all of them.
    """
    targets: dict[int, int] = {}
    opens: list[tuple[int, int]] = []  # (index, whitespace seen before it)
    spaces = 0
    pos = 0
    while pos < len(text):
        char = text[pos]
        if char == "\\" and text[pos + 1 : pos + 2] in _PUNCTUATION:
            pos += 2
            continue
        if char.isspace():
            spaces += 1
        elif char == "(":
            opens.append((pos, spaces))
        elif char == ")" and opens:
            start, seen = opens.pop()
            if seen == spaces:
                targets[start] = pos
        pos += 1
    return targets


def _run_end(text: str, pos: int) -> int:
    end = pos
    while end < len(text) and text[end] == text[pos]:
        end += 1
    return end


def _spaced(text: str, pos: int) -> bool:
    return pos < 0 or pos >= len(text) or text[pos].isspace()


def _literal_run(text: str, start: int, end: int) -> bool:
    return _spaced(text, start - 1) and _spaced(text, end)


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
        self.stack: list[int] = []  # indices of open tokens, innermost last
        self.active: dict[str, int] = {}
        self.buffer: list[str] = []
        self.run_end = 0  # end of the delimiter run being consumed
        self.lookahead: tuple[int, int] = (-1, 0)  # (run_end, next run length)
        self.targets: dict[int, int] | None = None

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
            elif char == "[":
                self._open("link", "[")
            elif char == "]" and self.active.get("link"):
                self._close_link()
            else:
                self._literal(char, 1)
        self._flush()
        self._demote(list(range(len(self.stack))))
        return self.tokens

    def _top(self) -> str:
        return self.tokens[self.stack[-1]].mark if self.stack else ""

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
        self.active[mark] = self.active.get(mark, 0) + 1
        self.pos += len(raw)

    def _close(self, raw: str) -> None:
        self._flush()
        mark = self.tokens[self.stack.pop()].mark
        self.active[mark] -= 1
        self.tokens.append(_Token("close", raw, mark))
        self.pos += len(raw)

    def _demote(self, depths: list[int]) -> None:
        """Turn the openers at these stack depths into literal text."""
        # Deepest last: every pop then shifts only the few entries above it.
        for depth in sorted(depths, reverse=True):
            index = self.stack.pop(depth)
            token = self.tokens[index]
            self.active[token.mark] -= 1
            self.tokens[index] = _Token("text", token.value)

    def _code(self) -> None:
        end = self.text.find("`", self.pos + 1)
        if end <= self.pos + 1:  # unclosed or empty: literal backtick
            self._literal("`", 1)
            return
        self._flush()
        self.tokens.append(_Token("code", self.text[self.pos + 1 : end]))
        self.pos = end + 1

    def _delimiter(self) -> None:
        text, pos = self.text, self.pos
        if pos >= self.run_end:  # first character of a new run
            self.run_end = _run_end(text, pos)
            if _literal_run(text, pos, self.run_end):
                self._literal(text[pos : self.run_end], self.run_end - pos)
                return
        top = self._top()
        if text[pos] == "~":
            if top == "strikethrough":
                self._close("~~")
            elif not self.active.get("strikethrough"):
                self._open("strikethrough", "~~")
            else:
                self._literal("~", 1)
            return
        remaining = self.run_end - pos
        strong, em = self.active.get("strong"), self.active.get("em")
        if top == "em" and remaining == 2 and not strong:
            self._open("strong", "**")  # em wraps strong: *a **b** c*
        elif top == "em":
            self._close("*")
        elif top == "strong" and remaining >= 2:
            self._close("**")
        elif remaining >= 3 and not strong and not em:
            if self._next_run_length() == 2:  # ***a** b*: strong closes first
                self._open("em", "*")
                self._open("strong", "**")
            else:
                self._open("strong", "**")
                self._open("em", "*")
        elif remaining >= 2 and not strong:
            self._open("strong", "**")
        elif not em:
            self._open("em", "*")
        else:
            self._literal("*", 1)

    def _next_run_length(self) -> int:
        """Length of the next non-literal ``*`` run after the current one."""
        if self.lookahead[0] != self.run_end:
            self.lookahead = (self.run_end, self._scan_next_run())
        return self.lookahead[1]

    def _scan_next_run(self) -> int:
        text, pos = self.text, self.run_end
        while pos < len(text):
            char = text[pos]
            if char == "\\" and text[pos + 1 : pos + 2] in _PUNCTUATION:
                pos += 2
            elif char == "`":
                end = text.find("`", pos + 1)
                pos = end + 1 if end > pos + 1 else pos + 1
            elif char == "*":
                end = _run_end(text, pos)
                if not _literal_run(text, pos, end):
                    return end - pos
                pos = end
            else:
                pos += 1
        return 0

    def _close_link(self) -> None:
        # At most three non-link marks can sit above the innermost "[".
        depth = len(self.stack) - 1
        while self.tokens[self.stack[depth]].mark != "link":
            depth -= 1
        start = self.pos + 1
        end = None
        if self.text[start : start + 1] == "(":
            if self.targets is None:
                self.targets = _link_targets(self.text)
            end = self.targets.get(start)
        if end is None:  # not a link: its "[" is literal text
            self._demote([depth])
            self._literal("]", 1)
            return
        # Marks opened inside the link text and still open there are literal.
        self._demote(list(range(depth + 1, len(self.stack))))
        self.tokens[self.stack[-1]].href = _unescape(self.text[start + 1 : end])
        self._close(self.text[self.pos : end + 1])
        # Links cannot nest: any enclosing "[" is literal text.
        if self.active.get("link"):
            self._demote(
                [d for d, i in enumerate(self.stack) if self.tokens[i].mark == "link"]
            )


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
