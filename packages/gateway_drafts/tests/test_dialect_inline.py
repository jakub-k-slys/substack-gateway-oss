from __future__ import annotations

import random
from typing import Any

import pytest
from _dialect_helpers import _t

from gateway_drafts.converters.dialect.inline import (
    escape_text,
    parse_inline,
    serialize_inline,
)


def _round_trip(content: list[dict[str, Any]]) -> list[dict[str, Any]]:
    md = serialize_inline(content)
    assert md is not None
    return parse_inline(md)


def test_bold_link_round_trips() -> None:
    content = [_t("see "), _t("docs", "strong", href="https://x")]
    assert _round_trip(content) == content


def test_bold_italic_and_strike() -> None:
    content = [_t("a", "strong", "em"), _t(" b "), _t("c", "strikethrough")]
    assert _round_trip(content) == content


def test_whitespace_inside_mark_is_kept() -> None:
    content = [_t("x"), _t(" bold ", "strong"), _t("y")]
    assert _round_trip(content) == content


def test_literal_tokens_stay_text() -> None:
    for raw in [
        "a * b",
        "use ::button here",
        "x {size=large}",
        "path\\to",
        "~~not~~ struck?",
    ]:
        content = [_t(raw)]
        assert _round_trip(content) == content


def test_inexpressible_returns_none() -> None:
    assert serialize_inline([_t("u", "underline")]) is None
    assert serialize_inline([_t("c", "code", "strong")]) is None
    assert (
        serialize_inline([{"type": "footnoteAnchor", "attrs": {"number": 1}}]) is None
    )
    odd = _t("l", href="https://x")
    odd["marks"][0]["attrs"]["rel"] = None
    assert serialize_inline([odd]) is None


def test_emoji_untouched() -> None:
    assert _round_trip([_t("🔁 share")]) == [_t("🔁 share")]


# --- beyond the brief -------------------------------------------------------


def test_escape_text_escapes_exactly_the_dialect_set() -> None:
    assert escape_text("\\*`[]~{}") == "\\\\\\*\\`\\[\\]\\~\\{\\}"
    assert escape_text("a_b (c) #d !e :f |g >h") == "a_b (c) #d !e :f |g >h"


def test_backslash_escapes_any_ascii_punctuation() -> None:
    assert parse_inline("\\#\\_\\(\\!") == [_t("#_(!")]
    # Not punctuation (or at the end): the backslash is literal.
    assert parse_inline("\\a \\é x\\") == [_t("\\a \\é x\\")]


def test_dialect_parser_accepts_inner_whitespace() -> None:
    assert parse_inline("a** x **b") == [_t("a"), _t(" x ", "strong"), _t("b")]
    assert parse_inline("x~~ y ~~z") == [_t("x"), _t(" y ", "strikethrough"), _t("z")]


@pytest.mark.parametrize(
    "raw",
    [
        "a ** b",
        "**open",
        "*a",
        "~~a",
        "~a~",
        "[a](x",
        "[a]",
        "[a] (x)",
        "`a",
        "``",
        "]",
        "**a *b**",
        "[**a](x)**",
        "***",
        "\\",
        "",
    ],
)
def test_parse_never_raises_and_unmatched_is_literal(raw: str) -> None:
    nodes = parse_inline(raw)
    for node in nodes:
        assert node["type"] == "text"
        assert node["text"]


def test_unmatched_delimiters_are_literal_text() -> None:
    assert parse_inline("a ** b") == [_t("a ** b")]
    assert parse_inline("**open") == [_t("**open")]
    assert parse_inline("[a](x") == [_t("[a](x")]
    assert parse_inline("`a") == [_t("`a")]
    assert parse_inline("") == []


def test_code_is_literal_and_round_trips() -> None:
    content = [_t("run "), _t("a*b\\c[d]", "code"), _t(" now")]
    assert serialize_inline(content) == "run `a*b\\c[d]` now"
    assert _round_trip(content) == content


def test_code_containing_backtick_is_not_expressible() -> None:
    assert serialize_inline([_t("a`b", "code")]) is None


def test_link_href_with_parentheses_and_backslash() -> None:
    href = "https://en.wikipedia.org/wiki/A_(b)\\c"
    content = [_t("wiki", href=href), _t(" (more)")]
    assert _round_trip(content) == content


def test_adjacent_links_with_different_hrefs() -> None:
    content = [_t("a", href="https://a"), _t("b", href="https://b")]
    assert serialize_inline(content) == "[a](https://a)[b](https://b)"
    assert _round_trip(content) == content


def test_marks_span_inside_one_link() -> None:
    content = [
        _t("x ", href="https://x"),
        _t("bold", "strong", href="https://x"),
        _t(" it", "strong", "em", href="https://x"),
        _t(" end", href="https://x"),
    ]
    assert serialize_inline(content) == "[x **bold* it*** end](https://x)"
    assert _round_trip(content) == content


def test_shared_marks_stay_open() -> None:
    content = [_t("a", "strong"), _t("b", "strong", "em"), _t("c", "strong")]
    assert serialize_inline(content) == "**a*b*c**"
    assert _round_trip(content) == content


@pytest.mark.parametrize(
    "content",
    [
        [_t("a", "strong"), _t("b", "em")],
        [_t("a", "em"), _t("b", "strong")],
        [_t("a", "em"), _t("b", "strong", "em")],
        [_t("a", "strong", "em"), _t("b", "em")],
        [_t("a*", "strong"), _t("b~", "strikethrough")],
        [_t("a\\", "em"), _t("*", "strong")],
        [_t("a", "em", href="https://x"), _t("b", "strong", "em", href="https://x")],
    ],
)
def test_adjacent_delimiter_runs_round_trip(content: list[dict[str, Any]]) -> None:
    assert _round_trip(content) == content


def test_link_with_non_default_class_is_not_expressible() -> None:
    node = _t("l", href="https://x")
    node["marks"][0]["attrs"]["class"] = "button"
    assert serialize_inline([node]) is None


def test_link_without_href_is_not_expressible() -> None:
    node = {"type": "text", "text": "l", "marks": [{"type": "link", "attrs": {}}]}
    assert serialize_inline([node]) is None


def test_non_canonical_content_fails_the_self_check() -> None:
    # em listed before strong: parse_inline always emits strong first.
    assert serialize_inline([_t("a", "em", "strong")]) is None
    # Adjacent nodes with identical marks: parse_inline would merge them.
    assert serialize_inline([_t("a", "strong"), _t("b", "strong")]) is None
    # Empty text node.
    assert serialize_inline([_t("")]) is None


def test_duplicate_or_malformed_marks_are_not_expressible() -> None:
    assert serialize_inline([_t("a", "strong", "strong")]) is None
    assert (
        serialize_inline([{"type": "text", "text": "a", "marks": ["strong"]}]) is None
    )
    assert serialize_inline([{"type": "text", "text": 1}]) is None


_ALPHABET = "ab \\*`[]~{}()_#!:é🔁"
_MARK_SETS: list[tuple[str, ...]] = [
    (),
    ("strong",),
    ("em",),
    ("strikethrough",),
    ("strong", "em"),
    ("strong", "strikethrough"),
    ("em", "strikethrough"),
    ("strong", "em", "strikethrough"),
]


def _random_content(
    rng: random.Random, *, spaced_marks: bool = False
) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = []
    for _ in range(rng.randint(1, 6)):
        length = rng.randint(1, 4)
        if rng.random() < 0.15:
            text = "".join(
                rng.choice(_ALPHABET.replace("`", "")) for _ in range(length)
            )
            node = _t(text, "code")
        else:
            text = "".join(rng.choice(_ALPHABET) for _ in range(length))
            href = rng.choice([None, None, "https://x", "https://y/(z)"])
            marks = rng.choice(_MARK_SETS)
            if marks and not spaced_marks:
                # A delimiter run with whitespace on both sides is literal, so
                # keep marked text from starting or ending with whitespace.
                text = text.strip() or "a"
            node = _t(text, *marks, href=href)
        if content and content[-1].get("marks") == node.get("marks"):
            content[-1]["text"] += node["text"]
        else:
            content.append(node)
    return content


def test_random_canonical_content_is_expressible_and_round_trips() -> None:
    rng = random.Random(20261018)
    for _ in range(3000):
        content = _random_content(rng)
        md = serialize_inline(content)
        assert md is not None, content
        assert parse_inline(md) == content


def test_parse_never_raises_on_random_delimiter_soup() -> None:
    rng = random.Random(7)
    soup = "a *~[]()`\\"
    for _ in range(3000):
        text = "".join(rng.choice(soup) for _ in range(rng.randint(0, 12)))
        nodes = parse_inline(text)
        for node in nodes:
            assert node["type"] == "text" and node["text"]


def test_many_unterminated_link_targets_parse_in_linear_time() -> None:
    # Each "](" without a closing ")" used to rescan to the end of the text.
    raw = "[a](" * 20000
    assert parse_inline(raw) == [_t(raw)]


def test_spaced_marked_text_is_the_only_reason_for_none() -> None:
    rng = random.Random(11)
    for _ in range(3000):
        content = _random_content(rng, spaced_marks=True)
        if serialize_inline(content) is None:
            assert any(
                node.get("marks")
                and node["text"] != node["text"].strip()
                and node["marks"][0]["type"] != "code"
                for node in content
            ), content


# --- review fix round 1 -----------------------------------------------------


def test_bracket_without_target_does_not_swallow_a_later_link() -> None:
    assert parse_inline("Note [1]: see [the docs](https://x) now") == [
        _t("Note [1]: see "),
        _t("the docs", href="https://x"),
        _t(" now"),
    ]


def test_stray_open_bracket_before_a_link_is_literal() -> None:
    assert parse_inline("see [a [docs](https://x)") == [
        _t("see [a "),
        _t("docs", href="https://x"),
    ]


def test_link_closing_inside_open_mark_makes_the_mark_literal() -> None:
    assert parse_inline("[**a](https://x)") == [_t("**a", href="https://x")]


def test_link_target_allows_balanced_parentheses() -> None:
    assert parse_inline("[wiki](https://en.wikipedia.org/wiki/A_(b)) ok") == [
        _t("wiki", href="https://en.wikipedia.org/wiki/A_(b)"),
        _t(" ok"),
    ]


def test_link_target_with_unbalanced_parentheses_is_not_a_link() -> None:
    assert parse_inline("[a](x(y) z") == [_t("[a](x(y) z")]


def test_link_title_does_not_land_in_the_href() -> None:
    assert parse_inline('[a](https://x "T")') == [_t('[a](https://x "T")')]


def test_href_with_whitespace_is_not_expressible() -> None:
    assert serialize_inline([_t("a", href="https://x y")]) is None


def test_spaced_delimiter_runs_are_literal() -> None:
    assert parse_inline("2 * 3 * 4 = 24") == [_t("2 * 3 * 4 = 24")]
    assert parse_inline("a ** b ** c") == [_t("a ** b ** c")]
    assert parse_inline("x ~~ y ~~ z") == [_t("x ~~ y ~~ z")]
    assert parse_inline("* a *") == [_t("* a *")]


def test_serializer_output_hitting_the_spaced_rule_returns_none() -> None:
    # Would be written "a * b*": the first run has spaces on both sides.
    assert serialize_inline([_t("a "), _t(" b", "em")]) is None


def test_em_wrapping_strong() -> None:
    assert parse_inline("*a **b** c*") == [
        _t("a ", "em"),
        _t("b", "strong", "em"),
        _t(" c", "em"),
    ]
    assert parse_inline("***a** b*") == [_t("a", "strong", "em"), _t(" b", "em")]


def test_many_open_brackets_then_closing_brackets_parse_in_linear_time() -> None:
    raw = "[" * 30000 + "]" * 30000
    assert parse_inline(raw) == [_t(raw)]


def test_long_asterisk_run_before_long_text_parses_in_linear_time() -> None:
    raw = "*" * 30000 + "a" * 30000 + "*"
    assert "".join(node["text"] for node in parse_inline(raw)).count("a") == 30000
