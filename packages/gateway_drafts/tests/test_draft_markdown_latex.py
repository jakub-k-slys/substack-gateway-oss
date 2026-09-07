"""Unit tests for LaTeX block support in the draft markdown converter.

Substack encodes display math as a block-level ``latex_block`` ProseMirror
node: ``{"type": "latex_block", "attrs": {"persistentExpression": "<tex>",
"id": "<10 uppercase letters>"}}``. The converter recognises ``$$ ... $$``
display-math delimiters and emits that node.
"""

from __future__ import annotations

import json
import re

from gateway_drafts.converters.markdown import (
    draft_body_to_markdown,
    markdown_to_draft_body,
)

_ID_RE = re.compile(r"^[A-Z]{10}$")


def _nodes(markdown: str) -> list[dict]:
    return json.loads(markdown_to_draft_body(markdown))["content"]


def _latex_blocks(markdown: str) -> list[dict]:
    return [n for n in _nodes(markdown) if n.get("type") == "latex_block"]


class TestLatexBlockNode:
    def test_single_line_display_math_becomes_latex_block(self) -> None:
        blocks = _latex_blocks("$$E = mc^2$$")
        assert len(blocks) == 1
        assert blocks[0]["attrs"]["persistentExpression"] == "E = mc^2"

    def test_node_has_random_uppercase_id(self) -> None:
        block = _latex_blocks("$$x$$")[0]
        assert _ID_RE.match(block["attrs"]["id"])

    def test_dirty_flag_is_not_emitted(self) -> None:
        # `dirty` is transient editor state; it must never be sent.
        block = _latex_blocks("$$x$$")[0]
        assert "dirty" not in block["attrs"]

    def test_multiline_fenced_block(self) -> None:
        markdown = "$$\nP(S) = 0.20\nP(\\neg S) = 0.80\n$$"
        blocks = _latex_blocks(markdown)
        assert len(blocks) == 1
        assert (
            blocks[0]["attrs"]["persistentExpression"]
            == "P(S) = 0.20\nP(\\neg S) = 0.80"
        )

    def test_backslashes_are_preserved(self) -> None:
        block = _latex_blocks(r"$$\frac{a}{b}$$")[0]
        assert block["attrs"]["persistentExpression"] == r"\frac{a}{b}"

    def test_two_blocks_get_distinct_ids(self) -> None:
        blocks = _latex_blocks("$$a$$\n\n$$b$$")
        assert len(blocks) == 2
        assert blocks[0]["attrs"]["id"] != blocks[1]["attrs"]["id"]


class TestLatexAmongOtherBlocks:
    def test_paragraphs_surrounding_latex_are_preserved(self) -> None:
        nodes = _nodes("Before\n\n$$E = mc^2$$\n\nAfter")
        types = [n["type"] for n in nodes]
        assert types == ["paragraph", "latex_block", "paragraph"]

    def test_dollar_dollar_inside_code_fence_is_literal(self) -> None:
        nodes = _nodes("```\n$$not latex$$\n```")
        assert [n["type"] for n in nodes] == ["highlighted_code_block"]
        assert _latex_blocks("```\n$$not latex$$\n```") == []


class TestLatexRoundTrip:
    def test_latex_block_renders_back_to_display_math(self) -> None:
        body = markdown_to_draft_body("$$E = mc^2$$")
        assert draft_body_to_markdown(body) == "$$\nE = mc^2\n$$"

    def test_round_trip_preserves_multiline_expression(self) -> None:
        original = "$$\na + b\nc + d\n$$"
        body = markdown_to_draft_body(original)
        assert draft_body_to_markdown(body) == original
