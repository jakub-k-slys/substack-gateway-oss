"""Fenced blocks of the draft dialect: code, Datawrapper, verbatim nodes, LaTeX.

A fence opens on a line of its own and closes on a line holding only its
closing delimiter. Body lines are kept exactly as written (no whitespace
stripping), so code and LaTeX survive unchanged.

- ```` ```lang {attrs} ```` … ```` ``` ```` → ``highlighted_code_block``.
- ```` ```datawrapper ```` + URL → ``_unresolved_datawrapper`` placeholder.
- ```` ```substack-node ```` + JSON → that node, verbatim.
- ``$$ {attrs}`` … ``$$`` (or ``$$expr$$`` on one line) → ``latex_block``.
"""

from __future__ import annotations

import json
import random
import re
import string
from dataclasses import dataclass, field
from typing import Any

from gateway_drafts.converters.dialect.attrs import (
    fill_defaults,
    loads_bounded_json,
    parse_attr_block,
)
from gateway_drafts.converters.dialect.errors import DraftMarkdownError

Node = dict[str, Any]

_CODE_OPEN = re.compile(r"^```([^\s`{]*)[ \t]*(?:\{(.*)\})?$")
_LATEX_OPEN = re.compile(r"^\$\$[ \t]*(?:\{(.*)\})?$")
_LATEX_ONE_LINE = re.compile(r"^\$\$(.+?)\$\$$")
HSPACE = " \t"  # the only whitespace the dialect strips around syntax
_VERBATIM = "substack-node"
_DATAWRAPPER = "datawrapper"
_DATAWRAPPER_ID = re.compile(
    r"datawrapper\.de/_/([A-Za-z0-9]+)|dwcdn\.net/([A-Za-z0-9]+)"
)


def normalize_datawrapper_url(url: str, line: int | None = None) -> str:
    """The resolve URL (``https://www.datawrapper.de/_/<id>/``) for a chart URL.

    Raises ``DraftMarkdownError`` (at ``line``, when known) for anything that is
    not a single published Datawrapper chart URL.
    """
    single_url = len(url.split()) == 1  # not empty, not several URLs
    match = _DATAWRAPPER_ID.search(url) if single_url else None
    if match is None:
        raise DraftMarkdownError(
            f"not a Datawrapper chart URL: {url!r}; a ```datawrapper fence holds "
            "one published chart URL, https://www.datawrapper.de/_/<id>/ or "
            "https://datawrapper.dwcdn.net/<id>/",
            line=line,
        )
    chart_id = match.group(1) or match.group(2)
    return f"https://www.datawrapper.de/_/{chart_id}/"


def attrs_at(text: str | None, line: int) -> dict[str, Any]:
    """Parse an attribute block body, reporting errors at ``line``."""
    if text is None:
        return {}
    try:
        return parse_attr_block(text)
    except DraftMarkdownError as exc:
        raise DraftMarkdownError(exc.message, line=line) from exc


@dataclass
class Fence:
    kind: str  # "code" | "datawrapper" | "substack-node" | "latex"
    line: int
    attrs: dict[str, Any]
    body: list[str] = field(default_factory=list)

    def closes_on(self, raw: str) -> bool:
        return raw.strip(HSPACE) == ("$$" if self.kind == "latex" else "```")

    def build(self) -> Node:
        text = "\n".join(self.body)
        if self.kind == "latex":
            return latex_block(text, self.attrs)
        if self.kind == _DATAWRAPPER:
            url = text.strip()
            # Validate here, where the fence's line is known.
            normalize_datawrapper_url(url, self.line)
            return {"type": "_unresolved_datawrapper", "attrs": {"url": url}}
        if self.kind == _VERBATIM:
            return _verbatim(text, self.line)
        node: Node = {
            "type": "highlighted_code_block",
            "attrs": fill_defaults("highlighted_code_block", self.attrs),
        }
        if text:  # ProseMirror forbids empty text nodes
            node["content"] = [{"type": "text", "text": text}]
        return node

    def unclosed(self) -> DraftMarkdownError:
        delimiter = "$$" if self.kind == "latex" else "```"
        return DraftMarkdownError(
            f"unclosed {self.kind} fence: close it with a line holding only {delimiter}",
            line=self.line,
        )


def open_fence(stripped: str, line: int) -> Fence | None:
    """Return the fence a line opens, or None when it opens none."""
    if match := _CODE_OPEN.match(stripped):
        lang, attr_text = match.group(1), match.group(2)
        attrs = attrs_at(attr_text, line)
        if lang in (_VERBATIM, _DATAWRAPPER):
            if attr_text is not None:
                raise DraftMarkdownError(
                    f"```{lang} fences take no attributes", line=line
                )
            return Fence(lang, line, {})
        return Fence("code", line, {"language": lang or None, **attrs})
    if stripped.startswith("```"):
        raise DraftMarkdownError(
            "malformed fence opener: write ```lang or ```lang {key=value} with "
            "nothing else on the line (start it with \\``` for literal text)",
            line=line,
        )
    if match := _LATEX_OPEN.match(stripped):
        return Fence("latex", line, attrs_at(match.group(1), line))
    return None


def one_line_latex(stripped: str) -> Node | None:
    """``$$expr$$`` on a single line, or None."""
    if match := _LATEX_ONE_LINE.match(stripped):
        return latex_block(match.group(1).strip(HSPACE), {})
    return None


def latex_id() -> str:
    """A 10-character uppercase id, matching Substack's editor-generated ids."""
    return "".join(random.choices(string.ascii_uppercase, k=10))


def latex_block(expression: str, attrs: dict[str, Any]) -> Node:
    full = {"persistentExpression": expression, **attrs}
    if "id" not in full:
        full["id"] = latex_id()
    return {"type": "latex_block", "attrs": full}


def _verbatim(text: str, line: int) -> Node:
    try:
        node = loads_bounded_json(text)
    except json.JSONDecodeError as exc:
        raise DraftMarkdownError(
            f"substack-node fence holds invalid JSON ({exc.msg} at fence body "
            f"line {exc.lineno}, column {exc.colno}); do not edit its JSON",
            line=line,
        ) from exc
    except (ValueError, RecursionError) as exc:  # e.g. too deep or huge numbers
        raise DraftMarkdownError(
            f"substack-node fence JSON cannot be read: {exc}", line=line
        ) from exc
    if not isinstance(node, dict) or not isinstance(node.get("type"), str):
        raise DraftMarkdownError(
            'substack-node fence must hold one JSON object with a "type"', line=line
        )
    if internal := _internal_type(node):
        raise DraftMarkdownError(
            f"substack-node fence holds the internal node type {internal!r}; "
            'node types starting with "_" are not allowed',
            line=line,
        )
    return node


def _internal_type(node: Any) -> str | None:
    """The first node ``type`` starting with ``_`` anywhere in ``node``, if any."""
    stack = [node]  # iterative: the JSON may be nested close to the stack limit
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            kind = item.get("type")
            if isinstance(kind, str) and kind.startswith("_"):
                return kind
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return None
