from __future__ import annotations

import pytest

from gateway_drafts.converters.dialect.attrs import (
    MARK_DEFAULTS,
    NODE_DEFAULTS,
    diff_from_defaults,
    fill_defaults,
    format_attr_block,
    parse_attr_block,
)
from gateway_drafts.converters.dialect.errors import DraftMarkdownError


def test_parse_typed_values() -> None:
    assert parse_attr_block("size=large width=1536 belowTheFold=false href=null x") == {
        "size": "large",
        "width": 1536,
        "belowTheFold": False,
        "href": None,
        "x": True,
    }


def test_parse_unquoted_edge_values() -> None:
    assert parse_attr_block("a=true b=-5 c=1.5 d=TRUE e=12ab") == {
        "a": True,
        "b": -5,
        "c": "1.5",
        "d": "TRUE",
        "e": "12ab",
    }


def test_parse_empty_and_whitespace() -> None:
    assert parse_attr_block("") == {}
    assert parse_attr_block("   \t ") == {}
    assert parse_attr_block("  a=1   b  ") == {"a": 1, "b": True}


def test_quoted_and_json_values() -> None:
    assert parse_attr_block('title="a \\"b\\" c" meta=\'{"k": [1]}\'') == {
        "title": 'a "b" c',
        "meta": {"k": [1]},
    }


def test_double_quoted_backslash_and_unknown_escape() -> None:
    assert parse_attr_block(r'p="C:\\dir" q="a\nb"') == {"p": "C:\\dir", "q": "a\\nb"}


def test_single_quoted_json_with_escaped_apostrophe() -> None:
    assert parse_attr_block(r"""v='"it\'s"'""") == {"v": "it's"}
    assert parse_attr_block(r"""v='"a\\"' w=1""") == {"v": "a\\", "w": 1}


def test_format_round_trips() -> None:
    attrs = {
        "title": "two words",
        "n": "123",
        "flag": True,
        "meta": {"k": [1]},
        "u": "https://x/y.png",
    }
    assert parse_attr_block(format_attr_block(attrs)[1:-1]) == attrs


def test_format_round_trips_awkward_values() -> None:
    attrs = {
        "empty": "",
        "t": "true",
        "f": "false",
        "nul": "null",
        "neg": "-3",
        "eq": "a=b",
        "braces": "{x}",
        "dq": 'say "hi"',
        "sq": "it's",
        "bs": "back\\slash",
        "nl": "line1\nline2",
        "float": 1.5,
        "none": None,
        "off": False,
        "num": 7,
        "lst": [1, "a", None],
        "uni": "zażółć gęślą",
    }
    block = format_attr_block(attrs)
    assert "\n" not in block
    assert parse_attr_block(block[1:-1]) == attrs


def test_format_shape() -> None:
    assert format_attr_block({}) == ""
    assert (
        format_attr_block({"a": True, "b": None, "c": 3, "d": "x y"})
        == '{a=true b=null c=3 d="x y"}'
    )


def test_format_rejects_invalid_key() -> None:
    with pytest.raises(DraftMarkdownError):
        format_attr_block({"bad key": 1})


@pytest.mark.parametrize(
    "text",
    ['a="unterminated', "a='[1", "a='{not json}'", "a=", "=x", 'a="x"y', "a='1'z"],
)
def test_malformed_blocks_raise(text: str) -> None:
    with pytest.raises(DraftMarkdownError):
        parse_attr_block(text)


@pytest.mark.parametrize(
    "text",
    ["n=" + "9" * 5000, "n=-" + "9" * 5000, "n='" + "9" * 5000 + "'"],
    ids=["unquoted", "negative", "json"],
)
def test_integer_too_long_to_convert_is_a_markdown_error(text: str) -> None:
    # Python refuses int <-> str conversion past 4300 digits (ValueError).
    with pytest.raises(DraftMarkdownError, match="'n'"):
        parse_attr_block(text)


def test_deeply_nested_json_value_is_a_markdown_error() -> None:
    with pytest.raises(DraftMarkdownError, match="'n'"):
        parse_attr_block("n='" + "[" * 100_000 + "]" * 100_000 + "'")


def test_long_digit_string_is_quoted_when_formatted() -> None:
    value = "9" * 5000
    assert format_attr_block({"n": value}) == '{n="' + value + '"}'
    assert parse_attr_block(format_attr_block({"n": value})[1:-1]) == {"n": value}


def test_diff_and_fill_are_inverse() -> None:
    full = fill_defaults("image2", {"src": "s", "imageSize": "large"})
    assert full["belowTheFold"] is False and full["imageSize"] == "large"
    assert diff_from_defaults("image2", full) == {"src": "s", "imageSize": "large"}


def test_unknown_key_survives() -> None:
    assert diff_from_defaults("paragraph", {"textAlign": None, "newKey": 1}) == {
        "newKey": 1
    }


def test_fill_does_not_mutate_tables() -> None:
    full = fill_defaults("heading", {"level": 2})
    full["extra"] = 1
    assert NODE_DEFAULTS["heading"] == {"level": 1, "textAlign": None}
    assert full == {"level": 2, "textAlign": None, "extra": 1}


def test_unknown_kind_has_no_defaults() -> None:
    assert fill_defaults("nope", {"a": 1}) == {"a": 1}
    assert diff_from_defaults("nope", {"a": 1}) == {"a": 1}


def test_diff_distinguishes_false_from_zero_and_none() -> None:
    assert diff_from_defaults("image2", {"belowTheFold": 0, "alt": ""}) == {
        "belowTheFold": 0,
        "alt": "",
    }
    assert (
        diff_from_defaults("ordered_list", {"start": 1, "order": 1, "type": None}) == {}
    )


def test_tables_contain_expected_kinds() -> None:
    assert set(NODE_DEFAULTS) == {
        "paragraph",
        "heading",
        "image2",
        "button",
        "highlighted_code_block",
        "latex_block",
        "pullquote",
        "ordered_list",
    }
    assert NODE_DEFAULTS["latex_block"] == {}
    assert MARK_DEFAULTS["link"] == {
        "target": "_blank",
        "rel": "noopener noreferrer nofollow",
        "class": None,
    }
    image = NODE_DEFAULTS["image2"]
    assert len(image) == 17
    assert all(image[k] is None for k in ("srcNoWatermark", "alt", "href", "align"))
    assert all(
        image[k] is False
        for k in ("belowTheFold", "topImage", "isProcessing", "offset")
    )


def test_error_message_has_line() -> None:
    assert str(DraftMarkdownError("bad", line=7)) == "line 7: bad"


def test_error_without_line() -> None:
    err = DraftMarkdownError("bad")
    assert str(err) == "bad"
    assert err.message == "bad" and err.line is None
    assert isinstance(err, ValueError)
    assert DraftMarkdownError("x", line=3).line == 3


def test_json_nesting_bound_is_independent_of_the_python_version() -> None:
    from gateway_drafts.converters.dialect.attrs import MAX_JSON_DEPTH

    ok = "[" * MAX_JSON_DEPTH + "]" * MAX_JSON_DEPTH
    assert parse_attr_block("n='" + ok + "'")["n"] is not None
    too_deep = "[" * (MAX_JSON_DEPTH + 1) + "]" * (MAX_JSON_DEPTH + 1)
    with pytest.raises(DraftMarkdownError, match="nested deeper"):
        parse_attr_block("n='" + too_deep + "'")
    # brackets inside JSON strings do not count towards the depth
    assert parse_attr_block("n='" + '["' + "[" * 500 + '"]' + "'") == {"n": ["[" * 500]}
