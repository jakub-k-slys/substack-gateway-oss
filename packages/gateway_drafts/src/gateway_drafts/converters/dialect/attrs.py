"""Attribute defaults table and ``{key=value}`` attribute blocks.

Substack ProseMirror nodes carry many attributes that are almost always at
their default value. The dialect omits attributes equal to the default
(``diff_from_defaults``) and restores them when parsing (``fill_defaults``).
Attributes that differ are written in an attribute block: whitespace-separated
``key`` / ``key=value`` items.
"""

from __future__ import annotations

import copy
import json
import re
from typing import Any

from gateway_drafts.converters.dialect.errors import DraftMarkdownError

# Real draft documents nest a few dozen levels at most. The explicit bound keeps
# deeply nested input an error on every Python version: older ``json`` modules
# raise RecursionError on it, newer ones parse it and leave the overflow to
# whatever walks the result later.
MAX_JSON_DEPTH = 200


def loads_bounded_json(text: str) -> Any:
    """``json.loads`` that refuses arrays/objects nested deeper than MAX_JSON_DEPTH.

    Raises ``ValueError`` (not ``JSONDecodeError``) when the bound is exceeded.
    """
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise ValueError(f"JSON nested deeper than {MAX_JSON_DEPTH} levels")
        elif char in "]}":
            depth -= 1
    return json.loads(text)


_IMAGE2_NONE_KEYS = (
    "srcNoWatermark",
    "fullscreen",
    "imageSize",
    "height",
    "width",
    "resizeWidth",
    "bytes",
    "alt",
    "title",
    "type",
    "href",
    "internalRedirect",
    "align",
)
_IMAGE2_FALSE_KEYS = ("belowTheFold", "topImage", "isProcessing", "offset")

NODE_DEFAULTS: dict[str, dict[str, Any]] = {
    "paragraph": {"textAlign": None},
    "heading": {"level": 1, "textAlign": None},
    "image2": {
        **dict.fromkeys(_IMAGE2_NONE_KEYS),
        **dict.fromkeys(_IMAGE2_FALSE_KEYS, False),
    },
    "button": {"action": None, "class": None},
    "highlighted_code_block": {"language": None, "nodeId": None},
    "latex_block": {},
    "pullquote": {"align": None, "color": None},
    "ordered_list": {"start": 1, "type": None, "order": 1},
}

MARK_DEFAULTS: dict[str, dict[str, Any]] = {
    "link": {
        "target": "_blank",
        "rel": "noopener noreferrer nofollow",
        "class": None,
    },
}


def _defaults_for(kind: str) -> dict[str, Any]:
    if kind in NODE_DEFAULTS:
        return NODE_DEFAULTS[kind]
    return MARK_DEFAULTS.get(kind, {})


def fill_defaults(kind: str, attrs: dict[str, Any]) -> dict[str, Any]:
    """Return the defaults for ``kind`` overlaid with ``attrs`` (unknown keys kept)."""
    return {**copy.deepcopy(_defaults_for(kind)), **attrs}


def diff_from_defaults(kind: str, attrs: dict[str, Any]) -> dict[str, Any]:
    """Return only the keys absent from the defaults or with a different value."""
    defaults = _defaults_for(kind)
    return {
        key: value
        for key, value in attrs.items()
        if key not in defaults or not _same(defaults[key], value)
    }


def _same(a: Any, b: Any) -> bool:
    # ``False == 0`` and ``True == 1`` in Python; attribute values must match by type too.
    return type(a) is type(b) and a == b


_INT = re.compile(r"-?\d+")
_NEEDS_QUOTES = re.compile(r"[\s\"'{}=]")
_KEY_FORBIDDEN = re.compile(r"[\s\"'{}=]")


def parse_attr_block(text: str) -> dict[str, Any]:
    """Parse the inside of an attribute block (without the braces)."""
    attrs: dict[str, Any] = {}
    pos = 0
    length = len(text)
    while pos < length:
        if text[pos].isspace():
            pos += 1
            continue
        start = pos
        while pos < length and not text[pos].isspace() and text[pos] != "=":
            pos += 1
        key = text[start:pos]
        if not key:
            raise DraftMarkdownError(
                f"attribute block: missing key before '=' in {text!r}"
            )
        if pos >= length or text[pos].isspace():
            attrs[key] = True
            continue
        pos += 1  # consume "="
        if pos >= length or text[pos].isspace():
            raise DraftMarkdownError(f"attribute block: missing value for '{key}'")
        attrs[key], pos = _parse_value(text, pos, key)
    return attrs


def _parse_value(text: str, pos: int, key: str) -> tuple[Any, int]:
    quote = text[pos]
    if quote not in ('"', "'"):
        end = pos
        while end < len(text) and not text[end].isspace():
            end += 1
        return _typed_literal(text[pos:end], key), end
    inner, end = _read_quoted(text, pos, key)
    if end < len(text) and not text[end].isspace():
        raise DraftMarkdownError(
            f"attribute block: unexpected text after quoted value of '{key}'"
        )
    if quote == '"':
        return inner, end
    try:
        return loads_bounded_json(inner), end
    except json.JSONDecodeError as exc:
        raise DraftMarkdownError(
            f"attribute block: invalid JSON for '{key}': {exc.msg}"
        ) from exc
    except (ValueError, RecursionError) as exc:  # e.g. too deep or huge numbers
        raise DraftMarkdownError(
            f"attribute block: JSON for '{key}' cannot be read: {exc}"
        ) from exc


def _read_quoted(text: str, pos: int, key: str) -> tuple[str, int]:
    """Read a quoted value starting at ``text[pos]``; return (unescaped text, index after)."""
    quote = text[pos]
    pos += 1
    out: list[str] = []
    while pos < len(text):
        char = text[pos]
        if char == quote:
            return "".join(out), pos + 1
        if char == "\\" and pos + 1 < len(text):
            nxt = text[pos + 1]
            if quote == '"' and nxt in ('"', "\\"):
                out.append(nxt)
            elif quote == "'" and nxt == "'":
                out.append(nxt)
            else:
                out.append(char + nxt)
            pos += 2
            continue
        out.append(char)
        pos += 1
    raise DraftMarkdownError(f"attribute block: unterminated {quote} quote for '{key}'")


_KEYWORDS: dict[str, Any] = {"true": True, "false": False, "null": None}


def _typed_literal(raw: str, key: str) -> Any:
    if raw in _KEYWORDS:
        return _KEYWORDS[raw]
    if _INT.fullmatch(raw):
        try:
            return int(raw)
        except ValueError as exc:  # past Python's int <-> str digit limit
            raise DraftMarkdownError(
                f"attribute block: integer value of '{key}' is too long ({exc})"
            ) from exc
    return raw


def _reads_as_literal(raw: str) -> bool:
    """Whether unquoted ``raw`` would parse as something other than a string."""
    return raw in _KEYWORDS or _INT.fullmatch(raw) is not None


def format_attr_block(attrs: dict[str, Any]) -> str:
    """Format ``attrs`` as ``{k=v ...}``; an empty mapping gives ``""``."""
    if not attrs:
        return ""
    parts: list[str] = []
    for key, value in attrs.items():
        if not key or _KEY_FORBIDDEN.search(key):
            raise DraftMarkdownError(f"attribute block: invalid key {key!r}")
        parts.append(f"{key}={_format_value(value)}")
    return "{" + " ".join(parts) + "}"


def _format_value(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return _format_string(value)
    return _format_json(value)


def _format_string(value: str) -> str:
    if "\n" in value or "\r" in value:
        return _format_json(value)
    if not value or _NEEDS_QUOTES.search(value) or _reads_as_literal(value):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def _format_json(value: Any) -> str:
    try:
        encoded = json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise DraftMarkdownError(
            f"attribute block: value is not JSON-serialisable: {exc}"
        ) from exc
    return "'" + encoded.replace("'", "\\'") + "'"
