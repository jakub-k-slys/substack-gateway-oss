from __future__ import annotations

import json
import re
from typing import Any

import pytest
from _dialect_helpers import _p, _t

from gateway_drafts.converters.dialect.attrs import fill_defaults
from gateway_drafts.converters.dialect.blocks import is_substack_hosted, parse_blocks
from gateway_drafts.converters.dialect.errors import DraftMarkdownError

_HOSTED = "https://substack-post-media.s3.amazonaws.com/public/images/a_1536x1024.png"


def _heading(text: str, level: int, align: str | None = None) -> dict[str, Any]:
    return {
        "type": "heading",
        "attrs": {"level": level, "textAlign": align},
        "content": [_t(text)],
    }


def _item(text: str, align: str | None = None) -> dict[str, Any]:
    return {"type": "list_item", "content": [_p(text, align)]}


# --- tests from the task brief ------------------------------------------------


def test_rule_and_buttons():
    nodes = parse_blocks(
        "---\n\n::button[Subscribe now]{href=subscribe}\n\n::button[Go]{href=https://x}"
    )
    assert nodes[0] == {"type": "horizontal_rule"}
    assert nodes[1]["attrs"] == {
        "url": "%%checkout_url%%",
        "text": "Subscribe now",
        "action": None,
        "class": None,
    }
    assert nodes[2]["attrs"]["url"] == "https://x"


def test_defaults_and_align_container():
    nodes = parse_blocks(
        "::defaults{align=justify}\n\nA\n\n:::align{center}\n# T\n\nB\n:::"
    )
    assert nodes[0] == _p("A", "justify")
    assert nodes[1]["attrs"] == {"level": 1, "textAlign": "center"}
    assert nodes[2] == _p("B", "center")


def test_callout():
    assert parse_blocks(":::callout\nX\n:::") == [
        {"type": "calloutBlock", "content": [_p("X")]}
    ]


def test_substack_node_verbatim():
    node = {"type": "digestPostEmbed", "attrs": {"id": 1, "title": "t"}}
    assert parse_blocks(
        "```substack-node\n" + json.dumps(node, indent=2) + "\n```"
    ) == [node]


def test_hosted_image_with_size_is_final():
    node = parse_blocks(f"![H]({_HOSTED}){{size=large}}")[0]
    img = node["content"][0]["attrs"]
    assert node["type"] == "captionedImage"
    assert (img["imageSize"], img["resizeWidth"], img["align"], img["fullscreen"]) == (
        "large",
        1200,
        "center",
        False,
    )


def test_watermark_instruction_is_placeholder():
    node = parse_blocks(f"![H]({_HOSTED}){{watermark=8%}}")[0]
    assert node["type"] == "_unresolved_image"
    assert node["attrs"]["watermark"] == {
        "scale": 0.08,
        "position": "top-right",
        "opacity": 65,
    }


def test_crlf_and_trailing_spaces():
    assert parse_blocks("A\r\n\r\n---   \r\n\r\nB") == parse_blocks("A\n\n---\n\nB")


def test_literal_rule_inside_sentence_is_text():
    assert parse_blocks("a --- b") == [_p("a --- b")]


@pytest.mark.parametrize(
    "bad, line",
    [
        (":::align{center}\nA", 1),
        ("A\n\n::defaults{align=justify}", 3),
        ("```substack-node\n{oops\n```", 1),
        (":::callout\n:::callout\nA\n:::\n:::", 2),
    ],
)
def test_errors_name_the_line(bad, line):
    with pytest.raises(DraftMarkdownError) as exc:
        parse_blocks(bad)
    assert exc.value.line == line


# --- ported behaviour of the previous converter ---------------------------------


def test_empty_input_gives_no_blocks():
    assert parse_blocks("") == []
    assert parse_blocks("\n\n   \n") == []


def test_paragraph_lines_are_joined_with_a_space():
    assert parse_blocks("one\ntwo  \n   three") == [_p("one two three")]


def test_paragraph_uses_inline_marks():
    assert parse_blocks("a **b** [c](https://x)") == [
        {
            "type": "paragraph",
            "attrs": {"textAlign": None},
            "content": [
                _t("a "),
                _t("b", "strong"),
                _t(" "),
                _t("c", href="https://x"),
            ],
        }
    ]


def test_headings():
    assert parse_blocks("# One\n## Two *x*\n###### Six") == [
        _heading("One", 1),
        {
            "type": "heading",
            "attrs": {"level": 2, "textAlign": None},
            "content": [_t("Two "), _t("x", "em")],
        },
        _heading("Six", 6),
    ]


def test_heading_needs_a_space_and_text():
    assert parse_blocks("#hashtag") == [_p("#hashtag")]
    assert parse_blocks("####### seven") == [_p("####### seven")]
    assert parse_blocks("#  ") == [_p("#")]


@pytest.mark.parametrize("marker", ["-", "*", "+"])
def test_bullet_list(marker):
    md = f"{marker} one\n{marker} **two**"
    assert parse_blocks(md) == [
        {
            "type": "bullet_list",
            "content": [
                _item("one"),
                {
                    "type": "list_item",
                    "content": [
                        {
                            "type": "paragraph",
                            "attrs": {"textAlign": None},
                            "content": [_t("two", "strong")],
                        }
                    ],
                },
            ],
        }
    ]


def test_ordered_list_has_default_attrs():
    assert parse_blocks("1. a\n2. b\n\n3. c") == [
        {
            "type": "ordered_list",
            "attrs": {"start": 1, "type": None, "order": 1},
            "content": [_item("a"), _item("b"), _item("c")],
        }
    ]


def test_list_kind_switch_and_paragraph_end_lists():
    nodes = parse_blocks("- a\n1. b\ntext\n- c")
    assert [n["type"] for n in nodes] == [
        "bullet_list",
        "ordered_list",
        "paragraph",
        "bullet_list",
    ]


def test_blockquote_and_pullquote():
    assert parse_blocks("> a\n>\n> b\n\n|> c") == [
        {"type": "blockquote", "content": [_p("a"), _p("b")]},
        {
            "type": "pullquote",
            "attrs": {"align": None, "color": None},
            "content": [_p("c")],
        },
    ]


def test_blank_line_between_quote_lines_keeps_one_quote():
    assert parse_blocks("> a\n\n> b") == [
        {"type": "blockquote", "content": [_p("a"), _p("b")]}
    ]


def test_quote_ends_at_a_non_quote_line():
    assert parse_blocks("> a\nb") == [
        {"type": "blockquote", "content": [_p("a")]},
        _p("b"),
    ]


def test_quote_body_is_parsed_recursively():
    assert parse_blocks("> # T\n> - x\n> > y") == [
        {
            "type": "blockquote",
            "content": [
                _heading("T", 1),
                {"type": "bullet_list", "content": [_item("x")]},
                {"type": "blockquote", "content": [_p("y")]},
            ],
        }
    ]


def test_code_fence():
    assert parse_blocks("```python\ndef f():  \n    return 1\n```") == [
        {
            "type": "highlighted_code_block",
            "attrs": {"language": "python", "nodeId": None},
            "content": [{"type": "text", "text": "def f():  \n    return 1"}],
        }
    ]


def test_code_fence_without_language_and_with_node_id():
    assert parse_blocks("```\nx\n```")[0]["attrs"] == {"language": None, "nodeId": None}
    node = parse_blocks("```python {nodeId=abc-123}\nx\n```   ")[0]
    assert node["attrs"] == {"language": "python", "nodeId": "abc-123"}


def test_code_fence_language_may_contain_punctuation():
    node = parse_blocks("```c++\nx\n```")[0]
    assert node["attrs"]["language"] == "c++"


def test_empty_code_fence_has_no_empty_text_node():
    assert parse_blocks("```\n```") == [
        {
            "type": "highlighted_code_block",
            "attrs": {"language": None, "nodeId": None},
        }
    ]


def test_block_syntax_inside_code_fence_is_literal():
    nodes = parse_blocks("```\n$$not latex$$\n:::\n::defaults{align=left}\n---\n```")
    assert [n["type"] for n in nodes] == ["highlighted_code_block"]
    assert nodes[0]["content"][0]["text"] == (
        "$$not latex$$\n:::\n::defaults{align=left}\n---"
    )


def test_datawrapper_fence_is_placeholder():
    assert parse_blocks(
        "```datawrapper\n https://www.datawrapper.de/_/boimj/ \n```"
    ) == [
        {
            "type": "_unresolved_datawrapper",
            "attrs": {"url": "https://www.datawrapper.de/_/boimj/"},
        }
    ]


def test_single_line_latex():
    node = parse_blocks("$$ E = mc^2 $$")[0]
    assert node["type"] == "latex_block"
    assert node["attrs"]["persistentExpression"] == "E = mc^2"
    assert re.fullmatch(r"[A-Z]{10}", node["attrs"]["id"])


def test_multiline_latex_keeps_lines_and_backslashes():
    node = parse_blocks("$$\nP(S) = 0.20  \nP(\\neg S)\n$$")[0]
    assert node["attrs"]["persistentExpression"] == "P(S) = 0.20  \nP(\\neg S)"


def test_latex_id_is_kept_when_given():
    assert parse_blocks("$$ {id=ABCDEFGHIJ}\nx\n$$") == [
        {
            "type": "latex_block",
            "attrs": {"persistentExpression": "x", "id": "ABCDEFGHIJ"},
        }
    ]


def test_generated_latex_ids_differ():
    a, b = parse_blocks("$$a$$\n\n$$b$$")
    assert a["attrs"]["id"] != b["attrs"]["id"]


def test_external_image_is_placeholder():
    assert parse_blocks("![A cat](https://x/cat.png)") == [
        {
            "type": "_unresolved_image",
            "attrs": {
                "src": "https://x/cat.png",
                "alt": "A cat",
                "image_attrs": {},
                "watermark": None,
            },
        }
    ]


def test_data_uri_image_is_parsed_whole():
    node = parse_blocks("![](data:image/png;base64,QUJDRA==)")[0]
    assert node["attrs"]["src"] == "data:image/png;base64,QUJDRA=="
    assert node["attrs"]["alt"] == ""


def test_image_inside_text_is_not_an_image():
    assert parse_blocks("see ![a](https://x/a.png)")[0]["type"] == "paragraph"


# --- new block syntax ---------------------------------------------------------


@pytest.mark.parametrize(
    "href, url",
    [
        ("share", "%%share_url%%"),
        ("comment", "%%half_magic_comments_url%%"),
        ('"https://x.test/a b"', "https://x.test/a b"),
    ],
)
def test_button_urls(href, url):
    node = parse_blocks(f"::button[Go]{{href={href}}}")[0]
    assert node == {
        "type": "button",
        "attrs": {"url": url, "text": "Go", "action": None, "class": None},
    }


def test_button_text_may_escape_a_bracket_and_extra_attrs_are_kept():
    node = parse_blocks(r"::button[a \] b]{href=share class=wide}")[0]
    assert node["attrs"] == {
        "url": "%%share_url%%",
        "text": "a ] b",
        "action": None,
        "class": "wide",
    }


@pytest.mark.parametrize(
    "md",
    [
        "::button[]{href=share}",
        "::button[Go]",
        "::button[Go]{class=x}",
        "::button{href=x}",
    ],
)
def test_button_needs_text_and_href(md):
    with pytest.raises(DraftMarkdownError) as exc:
        parse_blocks("A\n\n" + md)
    assert exc.value.line == 3


def test_attribute_value_with_unicode_line_separator_is_one_line():
    node = parse_blocks('::button[Go]{href="a b\x85c"}')[0]
    assert node["attrs"]["url"] == "a b\x85c"


def test_defaults_apply_to_nested_paragraphs_but_not_headings():
    md = "\n\n::defaults{align=justify}\n# H\n- a\n\n> q\n\n:::callout\nc\n:::"
    assert parse_blocks(md) == [
        _heading("H", 1),
        {"type": "bullet_list", "content": [_item("a", "justify")]},
        {"type": "blockquote", "content": [_p("q", "justify")]},
        {"type": "calloutBlock", "content": [_p("c", "justify")]},
    ]


def test_align_default_means_null_alignment():
    md = "::defaults{align=justify}\n\n:::align{default}\nA\n:::\n\nB"
    assert parse_blocks(md) == [_p("A"), _p("B", "justify")]


@pytest.mark.parametrize("value", ["left", "center", "right", "justify"])
def test_align_values(value):
    assert parse_blocks(f":::align{{{value}}}\nA\n:::") == [_p("A", value)]


def test_align_applies_to_lists_and_quotes_inside():
    md = ":::align{right}\n- a\n> b\n:::"
    assert parse_blocks(md) == [
        {"type": "bullet_list", "content": [_item("a", "right")]},
        {"type": "blockquote", "content": [_p("b", "right")]},
    ]


def test_align_inside_callout_and_quote():
    md = ":::callout\n:::align{center}\n## H\n:::\nB\n:::\n\n> :::align{right}\n> Q\n> :::"
    assert parse_blocks(md) == [
        {"type": "calloutBlock", "content": [_heading("H", 2, "center"), _p("B")]},
        {"type": "blockquote", "content": [_p("Q", "right")]},
    ]


def test_container_lines_with_trailing_spaces_and_blank_lines():
    md = ":::callout   \n\n\nX   \n\n\n:::   \n\n\n\nY"
    assert parse_blocks(md) == [
        {"type": "calloutBlock", "content": [_p("X")]},
        _p("Y"),
    ]


def test_lone_carriage_returns_split_lines():
    assert parse_blocks("A\r\rB") == [_p("A"), _p("B")]


def test_empty_callout_has_no_content_key():
    assert parse_blocks(":::callout\n:::") == [{"type": "calloutBlock"}]


def test_substack_node_inside_callout_and_quote():
    node = {"type": "videoEmbed", "attrs": {"id": "v"}}
    fence = "```substack-node\n" + json.dumps(node) + "\n```"
    assert parse_blocks(f":::callout\n{fence}\n:::") == [
        {"type": "calloutBlock", "content": [node]}
    ]
    quoted = "\n".join("> " + line for line in fence.split("\n"))
    assert parse_blocks(quoted) == [{"type": "blockquote", "content": [node]}]


def test_substack_node_is_not_touched_by_defaults():
    node = {"type": "paragraph", "content": [_t("x")]}
    md = "::defaults{align=justify}\n```substack-node\n" + json.dumps(node) + "\n```"
    assert parse_blocks(md) == [node]


def test_hosted_image_without_attrs_is_final():
    assert parse_blocks(f"![]({_HOSTED})") == [
        {
            "type": "captionedImage",
            "content": [
                {"type": "image2", "attrs": fill_defaults("image2", {"src": _HOSTED})}
            ],
        }
    ]


@pytest.mark.parametrize(
    "size, expected",
    [
        ("normal", ("normal", 0)),
        ("large", ("large", 1200)),
        ("full", ("full", None)),
    ],
)
def test_size_presets(size, expected):
    node = parse_blocks(f"![H](https://x/a.png){{size={size}}}")[0]
    assert node["attrs"]["image_attrs"] == {
        "imageSize": expected[0],
        "resizeWidth": expected[1],
        "align": "center",
        "fullscreen": False,
    }


def test_hosted_image_state_attrs():
    original = "https://substackcdn.com/image/o.png"
    node = parse_blocks(
        f'![H]({_HOSTED}){{size=full original={original} width=1536 title="a b"}}'
    )[0]
    assert node == {
        "type": "captionedImage",
        "content": [
            {
                "type": "image2",
                "attrs": fill_defaults(
                    "image2",
                    {
                        "src": _HOSTED,
                        "alt": "H",
                        "imageSize": "full",
                        "resizeWidth": None,
                        "align": "center",
                        "fullscreen": False,
                        "srcNoWatermark": original,
                        "width": 1536,
                        "title": "a b",
                    },
                ),
            }
        ],
    }


def test_watermark_options():
    node = parse_blocks(
        "![](https://x/a.png){original=https://x/o.png watermark "
        "watermark-pos=bottom-left watermark-opacity=40 size=normal}"
    )[0]
    assert node["attrs"] == {
        "src": "https://x/a.png",
        "alt": "",
        "image_attrs": {
            "imageSize": "normal",
            "resizeWidth": 0,
            "align": "center",
            "fullscreen": False,
            "srcNoWatermark": "https://x/o.png",
        },
        "watermark": {"scale": 0.06, "position": "bottom-left", "opacity": 40},
    }


def test_image_attribute_block_may_follow_a_space():
    node = parse_blocks("![](https://x/a.png) {size=large}")[0]
    assert node["attrs"]["image_attrs"]["imageSize"] == "large"


@pytest.mark.parametrize(
    "attrs",
    [
        "size=huge",
        "size",
        "watermark-pos=middle",
        "watermark watermark-opacity=101",
        "watermark watermark-opacity=-1",
        "watermark watermark-opacity=50%",
        "watermark=0%",
        "watermark=abc",
        "watermark=8",
        "watermark=-5%",
        "watermark-pos=top-left",
        "watermark-opacity=10",
        "original",
        'title="unterminated',
    ],
)
def test_bad_image_attributes_name_the_line(attrs):
    with pytest.raises(DraftMarkdownError) as exc:
        parse_blocks(f"A\n\n![](https://x/a.png){{{attrs}}}")
    assert exc.value.line == 3


@pytest.mark.parametrize(
    "md",
    [
        r"\# not a heading",
        r"\> not a quote",
        r"\|> not a pullquote",
        r"\- not a list",
        r"\+ not a list",
        r"\* not a list",
        r"1\. not a list",
        r"\::button[Go]{href=share}",
        r"\:::callout",
        r"\:::",
        r"\$$x$$",
        r"\```",
        r"\!\[a\](https://x/a.png)",
        r"\---",
        r"\::defaults{align=left}",
    ],
)
def test_escaped_block_syntax_is_paragraph_text(md):
    nodes = parse_blocks("A\n\n" + md)
    assert nodes[0] == _p("A")
    assert len(nodes) == 2
    assert nodes[1]["type"] == "paragraph"
    assert nodes[1]["content"] == [_t(md.replace("\\", ""))]


@pytest.mark.parametrize(
    "md",
    [
        "::buttons are fun",
        ":::alignment matters",
        "::note this",
        ":::note",
        "$$ is money",
        "```js title",
    ],
)
def test_lookalike_lines_are_paragraph_text(md):
    assert parse_blocks(md) == [_p(md)]


@pytest.mark.parametrize(
    "bad, line",
    [
        ("A\n\n```python\nx", 3),
        ("A\n\n$$\nx", 3),
        ("A\n\n```datawrapper\nhttps://x", 3),
        ("A\n:::", 2),
        ("A\n\n:::callout\nB", 3),
        (":::align{center}\n:::align{left}\nA\n:::\n:::", 2),
        (":::align{center}\n:::callout\nA\n:::\n:::", 2),
        (":::align{middle}\nA\n:::", 1),
        (":::align\nA\n:::", 1),
        (":::callout{x=1}\nA\n:::", 1),
        ("::defaults{align=justify}\n::defaults{align=left}", 2),
        ("::defaults{align=middle}", 1),
        ("::defaults{x=1}", 1),
        ("::defaults", 1),
        ("> A\n> ::defaults{align=left}", 2),
        ("A\n\n> :::callout\n> B\n> :::", 3),
        ("A\n\n> :::align{center}\n> B", 3),
        (":::align{center}\n> :::align{left}\n> B\n> :::\n:::", 2),
        ("A\n\n```substack-node\n[1, 2]\n```", 3),
        ('```substack-node\n{"attrs": {}}\n```', 1),
        ("```python {nodeId=}\n```", 1),
    ],
)
def test_more_errors_name_the_line(bad, line):
    with pytest.raises(DraftMarkdownError) as exc:
        parse_blocks(bad)
    assert exc.value.line == line


def test_substack_node_error_message_mentions_json():
    with pytest.raises(DraftMarkdownError, match="JSON"):
        parse_blocks("```substack-node\n{oops\n```")


def test_unclosed_container_inside_quote_reports_the_original_line():
    with pytest.raises(DraftMarkdownError) as exc:
        parse_blocks("A\n\nB\n\n> x\n> :::callout")
    assert exc.value.line == 6


@pytest.mark.parametrize(
    "src, hosted",
    [
        (_HOSTED, True),
        ("https://substackcdn.com/image/fetch/abc", True),
        ("HTTP://SUBSTACKCDN.COM/x.png", True),
        ("https://example.com/substackcdn.com/x.png", False),
        ("https://x/cat.png", False),
        ("data:image/png;base64,QUJD", False),
    ],
)
def test_is_substack_hosted(src, hosted):
    assert is_substack_hosted(src) is hosted


def test_only_spaces_and_tabs_count_as_strippable_whitespace():
    assert parse_blocks("a \t \n\n b\x85c") == [
        _p("a "),
        _p(" b\x85c"),
    ]


def test_lone_hash_is_paragraph_text_and_ends_the_list():
    assert parse_blocks("- a\n# \n- b") == [
        {"type": "bullet_list", "content": [_item("a")]},
        _p("#"),
        {"type": "bullet_list", "content": [_item("b")]},
    ]


def test_deeply_nested_quotes_raise_instead_of_overflowing_the_stack():
    assert parse_blocks("> " * 32 + "x")  # the limit itself is fine
    with pytest.raises(DraftMarkdownError) as exc:
        parse_blocks("A\n\n" + "> " * 400 + "x")
    assert exc.value.line == 3


@pytest.mark.parametrize(
    "body", ["[" * 100_000, '{"type": "x", "n": ' + "9" * 5000 + "}"]
)
def test_unreadable_substack_node_json_is_a_markdown_error(body):
    with pytest.raises(DraftMarkdownError) as exc:
        parse_blocks("A\n\n```substack-node\n" + body + "\n```")
    assert exc.value.line == 3
