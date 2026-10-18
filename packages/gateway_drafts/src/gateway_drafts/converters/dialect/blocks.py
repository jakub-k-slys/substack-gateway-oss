"""Block-level draft Markdown → Substack ProseMirror nodes.

``parse_blocks`` walks the input line by line. Lines are split on ``\\n`` only
(after normalising ``\\r\\n`` / ``\\r``), never with ``str.splitlines``:
attribute values may hold U+2028 and friends. Outside fences, trailing
whitespace (spaces and tabs) is ignored.

Block syntax, recognised only at the start of a line (a leading backslash
makes the line paragraph text):

- ``#``…``######`` headings, ``-`` / ``*`` / ``+`` and ``N.`` list items,
  ``>`` blockquote and ``|>`` pullquote (bodies parsed recursively);
- fences (see ``fences``) and ``$$`` LaTeX;
- ``---`` horizontal rule, ``![alt](src){attrs}`` image,
  ``::button[Text]{href=…}``, ``::defaults{align=X}`` (first line only);
- ``:::align{X}`` / ``:::callout`` containers closed by a bare ``:::``.

Every other line is paragraph text; consecutive ones join with a space.
Malformed dialect constructs raise ``DraftMarkdownError`` with the 1-based
line number of the input.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlsplit

from gateway_drafts.converters.dialect.attrs import fill_defaults
from gateway_drafts.converters.dialect.errors import DraftMarkdownError
from gateway_drafts.converters.dialect.fences import (
    HSPACE,
    Fence,
    attrs_at,
    one_line_latex,
    open_fence,
)
from gateway_drafts.converters.dialect.inline import parse_inline

Node = dict[str, Any]
Line = tuple[int, str]

# Images already re-hosted on Substack's own S3/CDN (e.g. uploaded earlier via
# the upload_image primitive). Re-posting a Substack-owned URL to the image
# endpoint returns a payload without the ``bytes`` field and keeps the same
# asset, so such an image is built directly instead of re-uploaded. The URL's
# host is compared exactly (``urlsplit(...).hostname`` is already lower-case):
# ``substackcdn.com`` or a subdomain of it, and the ``substack-post-media``
# bucket's virtual-hosted S3 endpoint, with or without a region.
_SUBSTACK_CDN = "substackcdn.com"
_SUBSTACK_S3 = re.compile(r"substack-post-media\.s3(?:\.[a-z0-9-]+)?\.amazonaws\.com")

_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*)")
_BULLET = re.compile(r"^[-*+][ \t]+(.*)")
_ORDERED = re.compile(r"^(\d+)\.[ \t]+(.*)")
_QUOTE = re.compile(r"^(>|\|>) ?(.*)")
_IMAGE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)(?:[ \t]*\{(.*)\})?$")
_DIRECTIVE = re.compile(r"^::(button|defaults)(?![\w-])(.*)$")
_CONTAINER = re.compile(r"^:::(align|callout)(?![\w-])(.*)$")
_BUTTON = re.compile(r"^\[((?:\\.|[^\\\]])*)\]\{(.*)\}$")
_ESCAPE = re.compile(r"\\([!-/:-@\[-`{-~])")
_WATERMARK_SCALE = re.compile(r"(\d+(?:\.\d+)?)%")

ALIGN_VALUES: dict[str, str | None] = {
    "left": "left",
    "center": "center",
    "right": "right",
    "justify": "justify",
    "default": None,
}
BUTTON_URLS = {
    "subscribe": "%%checkout_url%%",
    "share": "%%share_url%%",
    "comment": "%%half_magic_comments_url%%",
}
SIZE_PRESETS: dict[str, dict[str, Any]] = {
    "normal": {"imageSize": "normal", "resizeWidth": 0},
    "large": {"imageSize": "large", "resizeWidth": 1200},
    "full": {"imageSize": "full", "resizeWidth": None},
}
WATERMARK_POSITIONS = ("top-right", "top-left", "bottom-right", "bottom-left")
WATERMARK_DEFAULT_SCALE = 0.06
WATERMARK_DEFAULT_OPACITY = 65
MAX_QUOTE_DEPTH = 32


def is_substack_hosted(src: str) -> bool:
    """Whether ``src`` is an http(s) URL on one of Substack's own image hosts."""
    try:
        parts = urlsplit(src)
    except ValueError:  # e.g. an unbalanced IPv6 bracket
        return False
    host = parts.hostname
    if parts.scheme.lower() not in ("http", "https") or not host:
        return False
    if host == _SUBSTACK_CDN or host.endswith("." + _SUBSTACK_CDN):
        return True
    return _SUBSTACK_S3.fullmatch(host) is not None


def parse_blocks(markdown: str) -> list[Node]:
    """Parse draft dialect Markdown into top-level ProseMirror nodes."""
    text = markdown.replace("\r\n", "\n").replace("\r", "\n")
    lines = list(enumerate(text.split("\n"), start=1))
    return _Parser(lines, _Context()).parse()


@dataclass(frozen=True)
class _Context:
    default_align: str | None = None
    in_quote: bool = False
    in_align: bool = False
    align: str | None = None
    depth: int = 0  # quote nesting level


@dataclass
class _Frame:
    kind: str  # "root" | "callout" | "align"
    line: int = 0
    align: str | None = None
    nodes: list[Node] = field(default_factory=list)


class _Parser:
    def __init__(self, lines: list[Line], ctx: _Context) -> None:
        self.lines = lines
        self.ctx = ctx
        self.default_align = ctx.default_align
        self.frames = [_Frame("root")]
        self.fence: Fence | None = None
        self.seen_block = False
        self.para: list[str] = []
        self.list_kind: str | None = None
        self.list_items: list[Node] = []
        self.quote_kind: str | None = None
        self.quote_lines: list[Line] = []

    # --- driver -------------------------------------------------------------

    def parse(self) -> list[Node]:
        for number, raw in self.lines:
            self._line(number, raw)
        if self.fence is not None:
            raise self.fence.unclosed()
        self._flush()
        if len(self.frames) > 1:
            frame = self.frames[-1]
            raise DraftMarkdownError(
                f"unclosed :::{frame.kind} container: close it with a line "
                "holding only :::",
                line=frame.line,
            )
        return self.frames[0].nodes

    def _line(self, number: int, raw: str) -> None:
        if self.fence is not None:
            if self.fence.closes_on(raw):
                self._emit(self.fence.build())
                self.fence = None
            else:
                self.fence.body.append(raw)
            return
        text = raw.rstrip(HSPACE)
        stripped = text.lstrip(HSPACE)
        if not stripped:
            self._flush_para()
            if self.quote_kind:
                self.quote_lines.append((number, ""))
            return
        first = not self.seen_block
        self.seen_block = True
        if match := _QUOTE.match(raw.lstrip(HSPACE)):
            self._quote_line(number, match.group(1), match.group(2))
            return
        self._flush_quote()
        if not self._block(number, text, stripped, first):
            self._flush_list()
            self.para.append(stripped)

    def _block(self, number: int, text: str, stripped: str, first: bool) -> bool:
        """Handle a non-paragraph line; return False when it is paragraph text."""
        if match := _BULLET.match(text):
            return self._list_line("bullet", match.group(1))
        if match := _ORDERED.match(text):
            return self._list_line("ordered", match.group(2))
        node = self._leaf(number, text, stripped, first)
        if node is False:
            return False
        self._flush()
        if isinstance(node, dict):
            self._emit(node)
        return True

    def _leaf(self, number: int, text: str, stripped: str, first: bool) -> Node | bool:
        """Return a node to emit, True (handled, nothing to emit) or False
        (the line is paragraph text)."""
        if stripped == "---":
            return {"type": "horizontal_rule"}
        if stripped == ":::":
            self._flush()
            self._close_container(number)
            return True
        if stripped.startswith(":::"):
            return self._container(number, stripped)
        if stripped.startswith("::"):
            return self._directive(number, stripped, first)
        if match := _HEADING.match(text):
            return self._heading(len(match.group(1)), match.group(2).strip(HSPACE))
        if node := one_line_latex(stripped):
            return node
        if fence := open_fence(stripped, number):
            self._flush()
            self.fence = fence
            return True
        if match := _IMAGE.match(stripped):
            return _image(match.group(1), match.group(2), match.group(3), number)
        return False

    # --- emitting and flushing ----------------------------------------------

    def _emit(self, node: Node) -> None:
        self.frames[-1].nodes.append(node)

    def _flush(self) -> None:
        self._flush_para()
        self._flush_list()
        self._flush_quote()

    def _flush_para(self) -> None:
        joined = " ".join(self.para)
        self.para = []
        if joined and (content := parse_inline(joined)):
            self._emit(self._paragraph(content))

    def _flush_list(self) -> None:
        if self.list_items:
            node: Node = {"type": f"{self.list_kind}_list"}
            if self.list_kind == "ordered":
                node["attrs"] = fill_defaults("ordered_list", {})
            node["content"] = self.list_items
            self._emit(node)
        self.list_kind = None
        self.list_items = []

    def _flush_quote(self) -> None:
        kind, lines = self.quote_kind, self.quote_lines
        self.quote_kind = None
        self.quote_lines = []
        if not lines:
            return
        if self.ctx.depth >= MAX_QUOTE_DEPTH:
            raise DraftMarkdownError(
                f"quotes nest deeper than {MAX_QUOTE_DEPTH} levels", line=lines[0][0]
            )
        inside, align = self._align()
        ctx = _Context(self.default_align, True, inside, align, self.ctx.depth + 1)
        content = _Parser(lines, ctx).parse()
        if not content:
            return
        if kind == ">":
            self._emit({"type": "blockquote", "content": content})
        else:
            attrs = fill_defaults("pullquote", {})
            self._emit({"type": "pullquote", "attrs": attrs, "content": content})

    # --- alignment ------------------------------------------------------------

    def _align(self) -> tuple[bool, str | None]:
        """(inside an :::align container, its alignment)."""
        for frame in reversed(self.frames):
            if frame.kind == "align":
                return True, frame.align
        return self.ctx.in_align, self.ctx.align

    def _paragraph(self, content: list[Node]) -> Node:
        inside, align = self._align()
        text_align = align if inside else self.default_align
        return {
            "type": "paragraph",
            "attrs": {"textAlign": text_align},
            "content": content,
        }

    def _heading(self, level: int, text: str) -> Node:
        inside, align = self._align()
        attrs = {"level": level, "textAlign": align if inside else None}
        return {"type": "heading", "attrs": attrs, "content": parse_inline(text)}

    # --- lists and quotes ---------------------------------------------------

    def _list_line(self, kind: str, item: str) -> bool:
        self._flush_para()
        if self.list_kind != kind:
            self._flush_list()
            self.list_kind = kind
        if content := parse_inline(item.strip(HSPACE)):
            paragraph = self._paragraph(content)
            self.list_items.append({"type": "list_item", "content": [paragraph]})
        return True

    def _quote_line(self, number: int, kind: str, body: str) -> None:
        self._flush_para()
        self._flush_list()
        if self.quote_kind != kind:
            self._flush_quote()
            self.quote_kind = kind
        self.quote_lines.append((number, body))

    # --- containers and directives --------------------------------------------

    def _container(self, number: int, stripped: str) -> bool:
        match = _CONTAINER.match(stripped)
        if match is None:
            return False
        kind, rest = match.group(1), match.group(2)
        if rest[:1] not in ("", "{"):
            raise _malformed(f":::{kind}", number)
        self._flush()
        if kind == "callout":
            if rest:
                raise DraftMarkdownError(":::callout takes no attributes", line=number)
            if self.ctx.in_quote or len(self.frames) > 1:
                raise DraftMarkdownError(
                    ":::callout is allowed only at the top level, not inside a "
                    "quote or another container",
                    line=number,
                )
            self.frames.append(_Frame("callout", number))
            return True
        value = rest[1:-1].strip(HSPACE) if rest.endswith("}") else None
        if value not in ALIGN_VALUES:
            raise DraftMarkdownError(
                ":::align needs one of {left|center|right|justify|default}, "
                "e.g. :::align{center}",
                line=number,
            )
        if self._align()[0]:
            raise DraftMarkdownError(":::align containers do not nest", line=number)
        self.frames.append(_Frame("align", number, ALIGN_VALUES[value]))
        return True

    def _close_container(self, number: int) -> None:
        if len(self.frames) == 1:
            raise DraftMarkdownError(
                "::: closes no open container (write \\::: for literal text)",
                line=number,
            )
        frame = self.frames.pop()
        if frame.kind == "align":
            self.frames[-1].nodes.extend(frame.nodes)
            return
        node: Node = {"type": "calloutBlock"}
        if frame.nodes:
            node["content"] = frame.nodes
        self._emit(node)

    def _directive(self, number: int, stripped: str, first: bool) -> Node | bool:
        match = _DIRECTIVE.match(stripped)
        if match is None:
            return False
        if match.group(2)[:1] not in ("", "[", "{"):
            raise _malformed(f"::{match.group(1)}", number)
        if match.group(1) == "button":
            return _button(match.group(2), number)
        top_level = not self.ctx.in_quote and len(self.frames) == 1
        if not (first and top_level):
            raise DraftMarkdownError(
                "::defaults is allowed only once, as the first line", line=number
            )
        self.default_align = _defaults_align(match.group(2), number)
        return True


_FORMS = {
    "::button": "::button[Text]{href=URL}",
    "::defaults": "::defaults{align=X}",
    ":::align": ":::align{X}",
    ":::callout": ":::callout",
}


def _malformed(name: str, number: int) -> DraftMarkdownError:
    return DraftMarkdownError(
        f"malformed {name} line: write it as {_FORMS[name]} with no space before "
        f"{{ or [ and nothing after it (start the line with a backslash, "
        f"\\{name}, for literal text)",
        line=number,
    )


def _defaults_align(rest: str, number: int) -> str | None:
    attrs = attrs_at(rest[1:-1], number) if rest.endswith("}") else None
    value = attrs.get("align") if attrs is not None and len(attrs) == 1 else None
    if not isinstance(value, str) or value not in ALIGN_VALUES:
        raise DraftMarkdownError(
            "::defaults needs {align=left|center|right|justify|default}", line=number
        )
    return ALIGN_VALUES[value]


def _unescape(text: str) -> str:
    return _ESCAPE.sub(r"\1", text)


def _button(rest: str, number: int) -> Node:
    match = _BUTTON.match(rest)
    text = _unescape(match.group(1)) if match else ""
    attrs = attrs_at(match.group(2), number) if match else {}
    href = attrs.pop("href", None)
    if not text or not isinstance(href, str) or not href:
        raise DraftMarkdownError(
            "::button needs a text and an href: ::button[Text]{href=URL}, where "
            "URL may be subscribe, share or comment",
            line=number,
        )
    url = BUTTON_URLS.get(href, href)
    return {
        "type": "button",
        "attrs": fill_defaults("button", {"url": url, "text": text, **attrs}),
    }


def _image(alt: str, src: str, attr_text: str | None, number: int) -> Node:
    attrs = attrs_at(attr_text, number)
    image_attrs: dict[str, Any] = {}
    if "size" in attrs:
        size = attrs.pop("size")
        if not isinstance(size, str) or size not in SIZE_PRESETS:
            raise DraftMarkdownError(
                "image size must be normal, large or full", line=number
            )
        image_attrs.update(SIZE_PRESETS[size], align="center", fullscreen=False)
    if "original" in attrs:
        original = attrs.pop("original")
        if not isinstance(original, str) or not original:
            raise DraftMarkdownError("image original= needs a URL", line=number)
        image_attrs["srcNoWatermark"] = original
    watermark = _watermark(attrs, number)
    image_attrs.update(attrs)
    if watermark is None and is_substack_hosted(src):
        final = fill_defaults("image2", {**image_attrs, "src": src, "alt": alt or None})
        return {
            "type": "captionedImage",
            "content": [{"type": "image2", "attrs": final}],
        }
    return {
        "type": "_unresolved_image",
        "attrs": {
            "src": src,
            "alt": alt,
            "image_attrs": image_attrs,
            "watermark": watermark,
        },
    }


def _watermark(attrs: dict[str, Any], number: int) -> dict[str, Any] | None:
    """Pop the watermark keys from ``attrs`` and return the instruction."""
    if "watermark" not in attrs:
        if "watermark-pos" in attrs or "watermark-opacity" in attrs:
            raise DraftMarkdownError(
                "watermark-pos / watermark-opacity need watermark too", line=number
            )
        return None
    value = attrs.pop("watermark")
    scale = WATERMARK_DEFAULT_SCALE
    if value is not True:
        match = _WATERMARK_SCALE.fullmatch(value) if isinstance(value, str) else None
        percent = float(match.group(1)) if match else 0.0
        if not 0 < percent <= 100:
            raise DraftMarkdownError(
                "watermark takes no value or a percentage of the image width, "
                "e.g. watermark=8%",
                line=number,
            )
        scale = percent / 100
    position = attrs.pop("watermark-pos", "top-right")
    if position not in WATERMARK_POSITIONS:
        raise DraftMarkdownError(
            "watermark-pos must be one of " + ", ".join(WATERMARK_POSITIONS),
            line=number,
        )
    opacity = attrs.pop("watermark-opacity", WATERMARK_DEFAULT_OPACITY)
    if type(opacity) is not int or not 0 <= opacity <= 100:
        raise DraftMarkdownError(
            "watermark-opacity must be a whole number from 0 to 100", line=number
        )
    return {"scale": scale, "position": position, "opacity": opacity}
