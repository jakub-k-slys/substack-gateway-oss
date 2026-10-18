from __future__ import annotations

import json
from typing import Any

import pytest
from _dialect_helpers import _p, _t, doc_with_image

from gateway_drafts.converters.dialect.attrs import fill_defaults
from gateway_drafts.converters.dialect.blocks import parse_blocks
from gateway_drafts.converters.dialect.serialize import serialize_doc

_HOSTED = "https://substack-post-media.s3.amazonaws.com/public/images/a_1536x1024.png"
_FENCE = "```substack-node"


def _doc(*nodes: dict[str, Any]) -> dict[str, Any]:
    return {"type": "doc", "content": list(nodes)}


def _roundtrip(*nodes: dict[str, Any]) -> str:
    md = serialize_doc(_doc(*nodes))
    assert parse_blocks(md) == list(nodes)
    return md


def _heading(text: str, level: int = 1, align: str | None = None) -> dict[str, Any]:
    return {
        "type": "heading",
        "attrs": {"level": level, "textAlign": align},
        "content": [_t(text)],
    }


def _item(text: str, align: str | None = None) -> dict[str, Any]:
    return {"type": "list_item", "content": [_p(text, align)]}


def _bullets(*texts: str, align: str | None = None) -> dict[str, Any]:
    return {"type": "bullet_list", "content": [_item(t, align) for t in texts]}


def _ordered(*texts: str, **attrs: Any) -> dict[str, Any]:
    return {
        "type": "ordered_list",
        "attrs": fill_defaults("ordered_list", attrs),
        "content": [_item(t) for t in texts],
    }


def _quote(*content: dict[str, Any]) -> dict[str, Any]:
    return {"type": "blockquote", "content": list(content)}


def _pullquote(*content: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "pullquote",
        "attrs": fill_defaults("pullquote", {}),
        "content": list(content),
    }


def _code(text: str, language: str | None = None, **attrs: Any) -> dict[str, Any]:
    node: dict[str, Any] = {
        "type": "highlighted_code_block",
        "attrs": fill_defaults(
            "highlighted_code_block", {"language": language, **attrs}
        ),
    }
    if text:
        node["content"] = [{"type": "text", "text": text}]
    return node


def _latex(expression: str, latex_id: str = "ABCDEFGHIJ") -> dict[str, Any]:
    return {
        "type": "latex_block",
        "attrs": {"persistentExpression": expression, "id": latex_id},
    }


def _button(url: str, text: str) -> dict[str, Any]:
    return {
        "type": "button",
        "attrs": fill_defaults("button", {"url": url, "text": text}),
    }


def _image(**attrs: Any) -> dict[str, Any]:
    return doc_with_image(**{"src": _HOSTED, **attrs})["content"][0]


# --- tests from the task brief ------------------------------------------------


def test_defaults_line_and_exception():
    doc = {
        "type": "doc",
        "content": [_p("A", "justify"), _p("B", "justify"), _p("C", "right")],
    }
    md = serialize_doc(doc)
    assert md.splitlines()[0] == "::defaults{align=justify}"
    assert ":::align{right}\nC\n:::" in md


def test_watermarked_image_state():
    md = serialize_doc(
        doc_with_image(
            src="https://substack-post-media.s3.amazonaws.com/public/images/w_1536x1024.png",
            srcNoWatermark="https://substack-post-media.s3.amazonaws.com/public/images/o_1536x1024.png",
            imageSize="full",
            resizeWidth=None,
            align="center",
            fullscreen=False,
        )
    )
    assert (
        md
        == "![H](https://substack-post-media.s3.amazonaws.com/public/images/w_1536x1024.png){size=full original=https://substack-post-media.s3.amazonaws.com/public/images/o_1536x1024.png}"
    )


def test_unknown_node_falls_back():
    node = {"type": "videoEmbed", "attrs": {"id": "v"}}
    assert serialize_doc({"type": "doc", "content": [node]}).startswith(
        "```substack-node\n"
    )


def test_nested_list_falls_back():
    nested = {
        "type": "bullet_list",
        "content": [
            {
                "type": "list_item",
                "content": [_p("a"), {"type": "bullet_list", "content": []}],
            }
        ],
    }
    assert "```substack-node" in serialize_doc({"type": "doc", "content": [nested]})


def test_literal_rule_paragraph_is_escaped():
    doc = {"type": "doc", "content": [_p("---")]}
    assert parse_blocks(serialize_doc(doc)) == doc["content"]


# --- defaults and alignment ---------------------------------------------------


def test_no_defaults_line_when_most_paragraphs_are_unaligned():
    md = _roundtrip(_p("A"), _p("B"), _p("C", "center"))
    assert md == "A\n\nB\n\n:::align{center}\nC\n:::"


def test_tied_alignment_gives_no_defaults_line():
    md = _roundtrip(_p("A", "justify"), _p("B", "center"))
    assert not md.startswith("::defaults")


def test_defaults_count_nested_paragraphs():
    md = _roundtrip(_p("A"), _bullets("x", "y", align="justify"))
    assert md == "::defaults{align=justify}\n\n:::align{default}\nA\n:::\n\n- x\n- y"


def test_consecutive_exceptions_share_one_container():
    md = _roundtrip(
        _p("A", "justify"),
        _p("B", "justify"),
        _p("C", "center"),
        _heading("T", 2, "center"),
        _p("D", "justify"),
    )
    assert ":::align{center}\nC\n\n## T\n:::" in md


def test_headings_ignore_the_default():
    md = _roundtrip(_p("A", "justify"), _heading("H"), _heading("I", 1, "justify"))
    assert md == "::defaults{align=justify}\n\nA\n\n# H\n\n:::align{justify}\n# I\n:::"


def test_quote_with_mixed_alignment_groups_inside():
    md = _roundtrip(_quote(_p("a"), _p("b", "center")))
    assert md == "> a\n>\n> :::align{center}\n> b\n> :::"


def test_callout_groups_alignment_inside():
    md = _roundtrip(
        {"type": "calloutBlock", "content": [_heading("H", 2, "center"), _p("B")]}
    )
    assert md == ":::callout\n:::align{center}\n## H\n:::\n\nB\n:::"


def test_uniformly_aligned_quote_and_list_go_in_a_container():
    md = _roundtrip(
        _p("x"), _p("y"), _quote(_p("q", "right")), _bullets("a", align="right")
    )
    assert md == "x\n\ny\n\n:::align{right}\n> q\n\n- a\n:::"


def test_list_with_mixed_alignment_falls_back():
    node = {"type": "bullet_list", "content": [_item("a"), _item("b", "center")]}
    assert serialize_doc(_doc(node)).startswith(_FENCE)


def test_fallback_node_ignores_defaults():
    underlined = {
        "type": "paragraph",
        "attrs": {"textAlign": None},
        "content": [_t("u", "underline")],
    }
    md = _roundtrip(_p("A", "justify"), _p("B", "justify"), underlined)
    assert md.startswith("::defaults{align=justify}\n\nA\n\nB\n\n" + _FENCE)


def test_failing_group_member_falls_back_alone():
    underlined = {
        "type": "paragraph",
        "attrs": {"textAlign": "center"},
        "content": [_t("u", "underline")],
    }
    unaligned = [_p(text) for text in ("A", "A2", "A3", "A4")]
    md = _roundtrip(*unaligned, _p("B", "center"), underlined, _p("C", "center"))
    assert md.count(_FENCE) == 1
    assert ":::align{center}\nB\n:::" in md
    assert ":::align{center}\nC\n:::" in md


# --- adjacency ----------------------------------------------------------------


def test_two_adjacent_blockquotes_do_not_merge():
    md = _roundtrip(_quote(_p("a")), _quote(_p("b")))
    assert md == "> a\n\n:::align{default}\n> b\n:::"


def test_two_adjacent_pullquotes_do_not_merge():
    md = _roundtrip(_pullquote(_p("a")), _pullquote(_p("b")))
    assert md == "|> a\n\n:::align{default}\n|> b\n:::"


def test_blockquote_then_pullquote_stay_readable():
    md = _roundtrip(_quote(_p("a")), _pullquote(_p("b")))
    assert md == "> a\n\n|> b"


@pytest.mark.parametrize(
    "first,second,expected",
    [
        (_bullets("a"), _bullets("b"), "- a\n\n:::align{default}\n- b\n:::"),
        (_ordered("a"), _ordered("b"), "1. a\n\n:::align{default}\n1. b\n:::"),
    ],
)
def test_two_adjacent_lists_of_one_kind_do_not_merge(first, second, expected):
    assert _roundtrip(first, second) == expected


def test_three_adjacent_blockquotes_alternate_with_a_separator():
    md = _roundtrip(_quote(_p("a")), _quote(_p("b")), _quote(_p("c")))
    assert md == "> a\n\n:::align{default}\n> b\n:::\n\n> c"


def test_separator_uses_the_quote_alignment_under_a_default():
    md = _roundtrip(_quote(_p("a", "justify")), _quote(_p("b", "justify")))
    assert md == ("::defaults{align=justify}\n\n> a\n\n:::align{justify}\n> b\n:::")


def test_adjacent_quote_with_mixed_alignment_falls_back():
    # No single :::align value fits a quote with mixed alignments.
    second = _quote(_p("b"), _p("c", "center"))
    md = _roundtrip(_p("x"), _p("y"), _quote(_p("a")), second)
    assert md.count(_FENCE) == 1


def test_adjacent_quotes_inside_an_align_group_do_not_merge():
    unaligned = [_p(text) for text in ("x", "y", "z")]
    md = _roundtrip(*unaligned, _quote(_p("a", "center")), _quote(_p("b", "center")))
    assert _FENCE not in md
    assert md.count(":::align{center}") == 2


def test_adjacent_quotes_inside_a_callout_stay_readable():
    md = _roundtrip(
        {"type": "calloutBlock", "content": [_quote(_p("a")), _quote(_p("b"))]}
    )
    assert md == ":::callout\n> a\n\n:::align{default}\n> b\n:::\n:::"


def test_adjacent_lists_inside_a_callout_stay_readable():
    md = _roundtrip(
        {"type": "calloutBlock", "content": [_bullets("a"), _bullets("b"), _p("c")]}
    )
    assert md == ":::callout\n- a\n\n:::align{default}\n- b\n:::\n\nc\n:::"


def test_adjacent_quotes_inside_a_quote_stay_readable():
    md = _roundtrip(_quote(_quote(_p("a")), _quote(_p("b"))))
    assert md == "> > a\n>\n> :::align{default}\n> > b\n> :::"


def test_adjacent_quotes_inside_an_aligned_quote_fall_back():
    # Inside :::align the separator container cannot nest, so the block falls back.
    unaligned = [_p(text) for text in ("x", "y", "z", "w", "v")]
    inner = _quote(_quote(_p("a", "center")), _quote(_p("b", "center")))
    md = _roundtrip(*unaligned, inner)
    assert md.count(_FENCE) == 1


# --- block kinds ----------------------------------------------------------------


def test_ordered_list_with_other_start_falls_back():
    md = _roundtrip(_ordered("a", "b", start=3))
    assert md.startswith(_FENCE)


def test_ordered_list_with_default_attrs_is_markdown():
    assert _roundtrip(_ordered("a", "b")) == "1. a\n2. b"


@pytest.mark.parametrize("line", ["```", "```python", "  ```"])
def test_code_containing_a_fence_line_falls_back(line):
    md = _roundtrip(_code(f"a\n{line}\nb", "python"))
    assert md.startswith(_FENCE)


def test_code_block_with_node_id():
    md = _roundtrip(_code("print(1)\n\n  x  ", "python", nodeId="abc-1"))
    assert md == "```python {nodeId=abc-1}\nprint(1)\n\n  x  \n```"


def test_empty_code_block():
    assert _roundtrip(_code("")) == "```\n```"


def test_latex_id_is_kept():
    md = _roundtrip(_latex("a \\\\ b\nc", "QWERTYUIOP"))
    assert md == "$$ {id=QWERTYUIOP}\na \\\\ b\nc\n$$"


def test_latex_without_id_falls_back():
    node = {"type": "latex_block", "attrs": {"persistentExpression": "x"}}
    assert _roundtrip(node).startswith(_FENCE)


def test_horizontal_rule_and_buttons():
    md = _roundtrip(
        {"type": "horizontal_rule"},
        _button("%%checkout_url%%", "Subscribe now"),
        _button("%%share_url%%", "Share"),
        _button("%%half_magic_comments_url%%", "Leave a comment"),
        _button("https://x.example/a b", "Go ]here[ \\o/"),
    )
    assert md.split("\n\n") == [
        "---",
        "::button[Subscribe now]{href=subscribe}",
        "::button[Share]{href=share}",
        "::button[Leave a comment]{href=comment}",
        '::button[Go \\]here[ \\\\o/]{href="https://x.example/a b"}',
    ]


def test_button_with_extra_attrs():
    node = {
        "type": "button",
        "attrs": fill_defaults("button", {"url": "u", "text": "T", "action": "x"}),
    }
    assert _roundtrip(node) == "::button[T]{href=u action=x}"


def test_button_whose_url_is_a_preset_name_falls_back():
    assert _roundtrip(_button("subscribe", "S")).startswith(_FENCE)


def test_headings_and_inline_marks():
    para = {
        "type": "paragraph",
        "attrs": {"textAlign": None},
        "content": [_t("a "), _t("b", "strong"), _t(" "), _t("c", href="https://x")],
    }
    md = _roundtrip(_heading("H", 3), para)
    assert md == "### H\n\na **b** [c](https://x)"


def test_heading_level_out_of_range_falls_back():
    assert _roundtrip(_heading("H", 7)).startswith(_FENCE)


def test_image_without_attrs():
    assert _roundtrip(_image(alt=None)) == f"![]({_HOSTED})"


def test_image_raw_size_attrs_and_extras_are_ordered():
    md = _roundtrip(
        _image(
            imageSize="large",
            resizeWidth=800,
            align="center",
            fullscreen=False,
            srcNoWatermark=_HOSTED,
            width=1536,
            height=1024,
            bytes=1234,
        )
    )
    assert md == (
        f"![H]({_HOSTED}){{imageSize=large resizeWidth=800 align=center "
        f"fullscreen=false original={_HOSTED} bytes=1234 height=1024 width=1536}}"
    )


@pytest.mark.parametrize(
    "size,attrs",
    [
        ("normal", {"imageSize": "normal", "resizeWidth": 0}),
        ("large", {"imageSize": "large", "resizeWidth": 1200}),
        ("full", {"imageSize": "full", "resizeWidth": None}),
    ],
)
def test_image_size_presets(size, attrs):
    md = _roundtrip(_image(align="center", fullscreen=False, **attrs))
    assert md == f"![H]({_HOSTED}){{size={size}}}"


def test_external_image_falls_back():
    assert _roundtrip(_image(src="https://example.com/a.png")).startswith(_FENCE)


def test_image_with_caption_falls_back():
    node = _image()
    node["content"].append({"type": "caption", "content": [_t("c")]})
    assert _roundtrip(node).startswith(_FENCE)


@pytest.mark.parametrize("kind", ["datawrapper", "digestPostEmbed"])
def test_state_only_nodes_fall_back(kind):
    node = {"type": kind, "attrs": {"url": "https://x"}}
    md = _roundtrip(node)
    assert (
        md == _FENCE + "\n" + json.dumps(node, indent=2, ensure_ascii=False) + "\n```"
    )


def test_unknown_mark_and_empty_paragraph_fall_back():
    underlined = {
        "type": "paragraph",
        "attrs": {"textAlign": None},
        "content": [_t("u", "underline")],
    }
    empty = {"type": "paragraph", "attrs": {"textAlign": None}}
    md = _roundtrip(underlined, empty)
    assert md.count(_FENCE) == 2


def test_unknown_node_deep_inside_falls_back_the_top_level_block():
    node = _quote(_p("a"), {"type": "videoEmbed", "attrs": {"id": "v"}})
    assert _roundtrip(node).startswith(_FENCE)


# --- line-start escaping --------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "# x",
        "#x",
        "> x",
        "|> x",
        "- x",
        "-",
        "+ x",
        "* x",
        "1. x",
        "12. x",
        "::button",
        "::button[Go]{href=x}",
        "::defaults{align=left}",
        ":::",
        ":::align{center}",
        ":::callout",
        "```",
        "```python",
        "$$",
        "$$x$$",
        "!x",
        "![a](b)",
        "---",
        "--- x",
        "{size=large}",
        "a \\ b",
    ],
)
def test_paragraph_text_survives(text):
    md = _roundtrip(_p(text))
    assert _FENCE not in md
    md = _roundtrip(_quote(_p(text)))
    assert _FENCE not in md


def test_paragraph_text_survives_as_first_block_after_defaults():
    _roundtrip(_p("::defaults{align=left}", "justify"), _p("b", "justify"))


# --- whole documents and robustness -----------------------------------------------


def test_rich_document_round_trips_without_fallback():
    nodes = [
        _heading("Title", 1),
        _p("Intro", "justify"),
        _p("More **text**", "justify"),
        _p("Centered", "center"),
        _heading("Sub", 2, "center"),
        {"type": "horizontal_rule"},
        _bullets("one", "two", align="justify"),
        _ordered("first", "second"),
        _quote(_p("quoted", "justify"), _p("q2", "right")),
        _pullquote(_p("pulled", "justify")),
        {
            "type": "calloutBlock",
            "content": [_p("in callout", "justify"), _bullets("c")],
        },
        _code("x = 1", "python", nodeId="n1"),
        _latex("E = mc^2"),
        _image(imageSize="large", resizeWidth=1200, align="center", fullscreen=False),
        _button("%%checkout_url%%", "Subscribe now"),
        _p("# not a heading", "justify"),
        _p("Outro", None),
    ]
    md = serialize_doc(_doc(*nodes))
    assert parse_blocks(md) == nodes
    assert _FENCE not in md
    assert md.startswith("::defaults{align=justify}\n\n")


def test_mixed_document_round_trips():
    nodes = [
        _p("a", "justify"),
        {"type": "videoEmbed", "attrs": {"id": "v"}},
        _quote(_p("x")),
        _quote(_p("y")),
        _bullets("l"),
        {"type": "datawrapper", "attrs": {"url": "u"}},
        _bullets("m"),
        _ordered("o", start=2),
        _code("```", None),
        _p("b", "center"),
    ]
    _roundtrip(*nodes)


def test_bool_attr_is_not_confused_with_int():
    node = {
        "type": "ordered_list",
        "attrs": {"start": True, "type": None, "order": 1},
        "content": [_item("a")],
    }
    md = serialize_doc(_doc(node))
    assert md.startswith(_FENCE)
    assert parse_blocks(md)[0]["attrs"]["start"] is True


def test_empty_doc():
    assert serialize_doc({"type": "doc", "content": []}) == ""
    assert serialize_doc({"type": "doc"}) == ""


@pytest.mark.parametrize(
    "doc",
    [
        {},
        {"content": None},
        {"content": "text"},
        {"content": [1, "x", None, []]},
        {
            "content": [
                {"type": "heading", "attrs": {"level": 10**9}, "content": [_t("x")]}
            ]
        },
        {
            "content": [
                {"type": "heading", "attrs": {"level": "2"}, "content": [_t("x")]}
            ]
        },
        {"content": [{"type": "paragraph", "attrs": None, "content": None}]},
        {
            "content": [
                {
                    "type": "paragraph",
                    "attrs": {"textAlign": ["x"]},
                    "content": [_t("x")],
                }
            ]
        },
        {"content": [{"type": "bullet_list", "content": [None, {"content": "x"}]}]},
        {"content": [{"type": "captionedImage", "content": [{"attrs": {"src": 1}}]}]},
        {"content": [{"type": "button", "attrs": {"text": 1, "url": None}}]},
        {"content": [{"type": "highlighted_code_block", "attrs": {"language": 3}}]},
        {"content": [{"type": "latex_block", "attrs": {"id": {"a": 1}}}]},
        {"content": [{"type": "blockquote", "content": [{"type": "blockquote"}]}]},
        {"content": [{"type": "calloutBlock", "content": {"a": 1}}]},
        {"content": [{"type": None}, {"no": "type"}, {"type": "x", 1: 2}]},
        {
            "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "a\nb"}]}
            ]
        },
    ],
)
def test_never_raises(doc):
    assert isinstance(serialize_doc(doc), str)


def test_deeply_nested_quotes_fall_back_without_raising():
    node: dict[str, Any] = _p("x")
    for _ in range(200):
        node = _quote(node)
    md = serialize_doc(_doc(node))
    assert md.startswith(_FENCE)
