"""Substack ProseMirror doc → draft dialect Markdown, losslessly.

``serialize_doc`` writes every top-level block in readable dialect syntax when
it can and as a ```` ```substack-node ```` fence (the node's JSON) when it
cannot. Each block it writes is re-parsed with ``parse_blocks`` under the same
``::defaults`` line and compared with the original node; a mismatch replaces
the block with a fence, so ``parse_blocks(serialize_doc(doc))`` gives back
``doc["content"]`` by construction. A final whole-document check guards
against block interactions the per-block check cannot see.

Alignment: the most frequent paragraph ``textAlign`` (ties → none) becomes the
``::defaults{align=X}`` line; consecutive blocks whose paragraphs and headings
all share another alignment are wrapped in one ``:::align{X}`` container.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Callable, Iterator
from typing import Any

from gateway_drafts.converters.dialect.attrs import (
    diff_from_defaults,
    format_attr_block,
)
from gateway_drafts.converters.dialect.blocks import (
    ALIGN_VALUES,
    BUTTON_URLS,
    SIZE_PRESETS,
    parse_blocks,
)
from gateway_drafts.converters.dialect.fences import HSPACE
from gateway_drafts.converters.dialect.inline import serialize_inline

Node = dict[str, Any]

_ALIGN_NAMES = {value: name for name, value in ALIGN_VALUES.items()}
_BUTTON_HREFS = {url: name for name, url in BUTTON_URLS.items()}
_SIZE_KEYS = ("imageSize", "resizeWidth", "align", "fullscreen")
_LINE_START = ("#", ">", "|>", "-", "+", "::", "$$", "```", "!")
_ORDERED_START = re.compile(r"\d+\.")
# Node types whose Markdown merges with an adjacent block of the same type.
_MERGING = frozenset({"blockquote", "pullquote", "bullet_list", "ordered_list"})
_FENCE = "```substack-node"
_OUTSIDE = object()  # placement of a block that needs no ``:::align`` container
_INVALID = object()  # an alignment value the dialect cannot write


def serialize_doc(doc: dict[str, Any]) -> str:
    """Write a ProseMirror doc as draft dialect Markdown; never raises."""
    content = doc.get("content") if isinstance(doc, dict) else None
    if not isinstance(content, list) or not content:
        return ""
    try:
        markdown = _Serializer(content).run()
        if _identical(parse_blocks(markdown), content):
            return markdown
    except Exception:  # any failure degrades to verbatim fences
        pass
    return "\n\n".join(_fence(node) for node in content)


class _Serializer:
    def __init__(self, content: list[Any]) -> None:
        self.content = content
        self.default = _default_align(content)
        self.prefix = ""
        if self.default is not None:
            self.prefix = f"::defaults{{align={_ALIGN_NAMES[self.default]}}}"

    def run(self) -> str:
        blocks = [self.prefix] if self.prefix else []
        previous: str | None = None  # merge kind of the last readable block
        for align, nodes in _units(self.content, self.default, grouping=True):
            if align is not _OUTSIDE:
                blocks.extend(self._group(align, nodes))
                previous = None
                continue
            for node in nodes:
                kind = _merge_kind(node)
                markdown = _block(node, self.default, in_align=False)
                merges = kind is not None and kind == previous
                if (
                    markdown is not None
                    and not merges
                    and self._check(markdown, [node])
                ):
                    blocks.append(markdown)
                    previous = kind
                else:
                    blocks.append(_fence(node))
                    previous = None
        return "\n\n".join(blocks)

    def _group(self, align: str | None, nodes: list[Node]) -> list[str]:
        """One ``:::align`` container per run of nodes that serialize together."""
        out: list[str] = []
        run: list[tuple[Node, str]] = []
        for node in nodes:
            markdown = _block(node, self.default, in_align=True)
            if run and (kind := _merge_kind(node)) and kind == _merge_kind(run[-1][0]):
                out.extend(self._run(align, run))
                run = []
            if markdown is None:
                out.extend(self._run(align, run))
                out.append(_fence(node))
                run = []
            else:
                run.append((node, markdown))
        out.extend(self._run(align, run))
        return out

    def _run(self, align: str | None, run: list[tuple[Node, str]]) -> list[str]:
        if not run:
            return []
        markdown = _container(align, [md for _, md in run])
        if self._check(markdown, [node for node, _ in run]):
            return [markdown]
        if len(run) == 1:
            return [_fence(run[0][0])]
        return [part for item in run for part in self._run(align, [item])]

    def _check(self, markdown: str, nodes: list[Node]) -> bool:
        text = f"{self.prefix}\n\n{markdown}" if self.prefix else markdown
        try:
            return _identical(parse_blocks(text), nodes)
        except Exception:  # unparseable output is a mismatch
            return False


# --- alignment ----------------------------------------------------------------


def _walk(node: Any) -> Iterator[dict[str, Any]]:
    """Yield ``node`` and every dict node below it through ``content`` lists."""
    stack = [node]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            yield item
            children = item.get("content")
            if isinstance(children, list):
                stack.extend(reversed(children))


def _align_of(node: Node) -> Any:
    attrs = node.get("attrs")
    value = attrs.get("textAlign") if isinstance(attrs, dict) else None
    if value is None or (isinstance(value, str) and value in _ALIGN_NAMES):
        return value
    return _INVALID


def _default_align(content: list[Any]) -> str | None:
    counts: Counter[Any] = Counter()
    for top in content:
        for node in _walk(top):
            if node.get("type") == "paragraph":
                counts[_align_of(node)] += 1
    ranked = counts.most_common(2)
    if not ranked or (len(ranked) == 2 and ranked[0][1] == ranked[1][1]):
        return None
    value = ranked[0][0]
    return value if value is not _INVALID else None


def _placement(node: Any, default: str | None) -> Any:
    """``_OUTSIDE`` or the alignment of the ``:::align`` container ``node`` needs."""
    paragraphs: set[Any] = set()
    headings: set[Any] = set()
    for item in _walk(node):
        if item.get("type") == "paragraph":
            paragraphs.add(_align_of(item))
        elif item.get("type") == "heading":
            headings.add(_align_of(item))
    if paragraphs <= {default} and headings <= {None}:
        return _OUTSIDE
    together = paragraphs | headings
    if len(together) != 1 or node.get("type") == "calloutBlock":
        return _OUTSIDE  # containers group inside; anything else falls back
    align = next(iter(together))
    return _OUTSIDE if align is _INVALID else align


def _units(
    nodes: list[Any], default: str | None, grouping: bool
) -> list[tuple[Any, list[Any]]]:
    """Consecutive nodes with the same placement, in order."""
    units: list[tuple[Any, list[Any]]] = []
    for node in nodes:
        align = _placement(node, default) if grouping else _OUTSIDE
        if units and units[-1][0] == align:
            units[-1][1].append(node)
        else:
            units.append((align, [node]))
    return units


def _container(align: str | None, parts: list[str]) -> str:
    body = "\n\n".join(parts)
    return f":::align{{{_ALIGN_NAMES[align]}}}\n{body}\n:::"


def _merge_kind(node: Any) -> str | None:
    kind = node.get("type") if isinstance(node, dict) else None
    return kind if kind in _MERGING else None


# --- blocks -----------------------------------------------------------------------


def _block(node: Any, default: str | None, in_align: bool) -> str | None:
    """Readable Markdown for one block, or None when the dialect cannot write it."""
    if not isinstance(node, dict):
        return None
    writer = _WRITERS.get(str(node.get("type")))
    if writer is None:
        return None
    try:
        return writer(node, default, in_align)
    except Exception:  # odd attribute shapes fall back
        return None


def _children(nodes: Any, default: str | None, in_align: bool) -> str | None:
    """Blocks inside a quote or callout, joined by blank lines."""
    if not isinstance(nodes, list):
        return None
    parts: list[str] = []
    previous: str | None = None
    for align, members in _units(nodes, default, grouping=not in_align):
        inside = align is not _OUTSIDE
        inner: list[str] = []
        for node in members:
            kind = _merge_kind(node)
            markdown = _block(node, default, in_align or inside)
            if markdown is None or (kind and kind == previous):
                return None
            inner.append(markdown)
            previous = kind
        parts.extend([_container(align, inner)] if inside else inner)
        if inside:
            previous = None
    return "\n\n".join(parts)


def _escape_line_start(markdown: str) -> str:
    if match := _ORDERED_START.match(markdown):
        return markdown[: match.end() - 1] + "\\" + markdown[match.end() - 1 :]
    if markdown.startswith(_LINE_START):
        return "\\" + markdown
    return markdown


def _inline(node: Node) -> str | None:
    content = node.get("content")
    if not isinstance(content, list) or not content:
        return None
    return serialize_inline(content)


def _paragraph(node: Node, default: str | None, in_align: bool) -> str | None:
    inline = _inline(node)
    return None if inline is None else _escape_line_start(inline)


def _heading(node: Node, default: str | None, in_align: bool) -> str | None:
    level = node["attrs"]["level"]
    inline = _inline(node)
    if type(level) is not int or not 1 <= level <= 6 or inline is None:
        return None
    return "#" * level + " " + inline


def _list(node: Node, default: str | None, in_align: bool) -> str | None:
    lines: list[str] = []
    for number, item in enumerate(node["content"], start=1):
        marker = f"{number}." if node["type"] == "ordered_list" else "-"
        paragraphs = item["content"]
        if len(paragraphs) != 1 or paragraphs[0].get("type") != "paragraph":
            return None
        inline = _inline(paragraphs[0])
        if inline is None:
            return None
        lines.append(f"{marker} {inline}")
    return "\n".join(lines) or None


def _quote(node: Node, default: str | None, in_align: bool) -> str | None:
    marker = ">" if node["type"] == "blockquote" else "|>"
    inner = _children(node.get("content"), default, in_align)
    if not inner:
        return None
    return "\n".join(
        f"{marker} {line}" if line else marker for line in inner.split("\n")
    )


def _callout(node: Node, default: str | None, in_align: bool) -> str | None:
    inner = _children(node.get("content", []), default, in_align)
    if inner is None:
        return None
    return f":::callout\n{inner}\n:::" if inner else ":::callout\n:::"


def _button(node: Node, default: str | None, in_align: bool) -> str | None:
    attrs = dict(node["attrs"])
    text, url = attrs.pop("text"), attrs.pop("url")
    if not isinstance(text, str) or not isinstance(url, str):
        return None
    label = text.replace("\\", "\\\\").replace("]", "\\]")
    extra = diff_from_defaults("button", attrs)
    block = format_attr_block({"href": _BUTTON_HREFS.get(url, url), **extra})
    return f"::button[{label}]{block}"


def _image(node: Node, default: str | None, in_align: bool) -> str | None:
    (image,) = node["content"]
    attrs = image["attrs"]
    src, alt = attrs["src"], attrs.get("alt")
    if not isinstance(src, str) or not (alt is None or isinstance(alt, str)):
        return None
    rest = diff_from_defaults("image2", attrs)
    rest.pop("src")
    rest.pop("alt", None)
    sizes = {key: rest.pop(key) for key in _SIZE_KEYS if key in rest}
    preset = _size_preset(attrs)
    ordered: dict[str, Any] = {"size": preset} if preset else sizes
    if "srcNoWatermark" in rest:
        ordered["original"] = rest.pop("srcNoWatermark")
    ordered.update((key, rest[key]) for key in sorted(rest))
    return f"![{alt or ''}]({src}){format_attr_block(ordered)}"


def _size_preset(attrs: Node) -> str | None:
    if attrs.get("align") != "center" or attrs.get("fullscreen") is not False:
        return None
    for name, preset in SIZE_PRESETS.items():
        if all(_identical(attrs.get(key), value) for key, value in preset.items()):
            return name
    return None


def _code(node: Node, default: str | None, in_align: bool) -> str | None:
    attrs = node["attrs"]
    language = attrs.get("language")
    text = ""
    if "content" in node:
        (child,) = node["content"]
        text = child["text"]
    if not isinstance(text, str) or not (language is None or isinstance(language, str)):
        return None
    if any(line.lstrip(HSPACE).startswith("```") for line in text.split("\n")):
        return None
    extra = diff_from_defaults("highlighted_code_block", attrs)
    extra.pop("language", None)
    block = format_attr_block(extra)
    opener = "```" + (language or "") + (f" {block}" if block else "")
    return opener + "\n" + (f"{text}\n" if text else "") + "```"


def _latex(node: Node, default: str | None, in_align: bool) -> str | None:
    attrs = dict(node["attrs"])
    expression = attrs.pop("persistentExpression")
    if not isinstance(expression, str) or "id" not in attrs:
        return None  # without an id the parser would generate a new one
    opener = f"$$ {format_attr_block(attrs)}"
    return opener + "\n" + (f"{expression}\n" if expression else "") + "$$"


_WRITERS: dict[str, Callable[[Node, str | None, bool], str | None]] = {
    "paragraph": _paragraph,
    "heading": _heading,
    "bullet_list": _list,
    "ordered_list": _list,
    "blockquote": _quote,
    "pullquote": _quote,
    "calloutBlock": _callout,
    "horizontal_rule": lambda node, default, in_align: "---",
    "button": _button,
    "captionedImage": _image,
    "highlighted_code_block": _code,
    "latex_block": _latex,
}


# --- verbatim fallback and comparison --------------------------------------------


def _fence(node: Any) -> str:
    try:
        body = json.dumps(node, indent=2, ensure_ascii=False, default=repr)
    except Exception:  # e.g. circular or absurdly deep input
        body = "null"
    return f"{_FENCE}\n{body}\n```"


def _identical(a: Any, b: Any) -> bool:
    """Equality that also requires equal types (``True`` is not ``1``)."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(_identical(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(map(_identical, a, b))
    return a == b
