"""Unit tests for converters.markdown.

These test markdown_to_doc (the pure document builder) and
markdown_to_note_payload (the envelope wrapper) in isolation,
without going through the HTTP/BDD stack.
"""

from __future__ import annotations

import pytest
from gateway_oss.converters.markdown import markdown_to_doc, markdown_to_note_payload

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _paragraphs(doc: dict) -> list:
    return doc["content"]


def _nodes(doc: dict, para: int) -> list:
    """1-indexed paragraph → its content nodes."""
    return _paragraphs(doc)[para - 1]["content"]


def _text_node(doc: dict, para: int, node: int) -> dict:
    """1-indexed paragraph + node → the node dict."""
    return _nodes(doc, para)[node - 1]


# ---------------------------------------------------------------------------
# markdown_to_doc — document structure
# ---------------------------------------------------------------------------


class TestDocStructure:
    def test_single_paragraph(self):
        doc = markdown_to_doc("Hello world")
        assert doc["type"] == "doc"
        assert doc["attrs"]["schemaVersion"] == "v1"
        assert len(_paragraphs(doc)) == 1

    def test_two_paragraphs_separated_by_blank_line(self):
        doc = markdown_to_doc("First\n\nSecond")
        assert len(_paragraphs(doc)) == 2

    def test_paragraph_type(self):
        doc = markdown_to_doc("Hello")
        assert _paragraphs(doc)[0]["type"] == "paragraph"

    def test_text_node_type(self):
        doc = markdown_to_doc("Hello")
        node = _text_node(doc, 1, 1)
        assert node["type"] == "text"
        assert node["text"] == "Hello"


# ---------------------------------------------------------------------------
# markdown_to_doc — inline formatting
# ---------------------------------------------------------------------------


class TestInlineFormatting:
    def test_plain_text_has_no_marks(self):
        doc = markdown_to_doc("plain text")
        node = _text_node(doc, 1, 1)
        assert "marks" not in node

    def test_bold(self):
        doc = markdown_to_doc("**bold**")
        node = _text_node(doc, 1, 1)
        assert node["text"] == "bold"
        assert node["marks"] == [{"type": "bold"}]

    def test_italic(self):
        doc = markdown_to_doc("*italic*")
        node = _text_node(doc, 1, 1)
        assert node["text"] == "italic"
        assert node["marks"] == [{"type": "italic"}]

    def test_code(self):
        doc = markdown_to_doc("`code`")
        node = _text_node(doc, 1, 1)
        assert node["text"] == "code"
        assert node["marks"] == [{"type": "code"}]

    def test_link(self):
        doc = markdown_to_doc("[label](https://example.com)")
        node = _text_node(doc, 1, 1)
        assert node["text"] == "label (https://example.com)"
        assert "marks" not in node

    def test_bold_adjacent_to_italic_preserves_space(self):
        doc = markdown_to_doc("**bold** *italic*")
        nodes = _nodes(doc, 1)
        # bold node, space node, italic node
        assert nodes[0]["text"] == "bold"
        assert nodes[0]["marks"] == [{"type": "bold"}]
        assert nodes[1]["text"] == " "
        assert "marks" not in nodes[1]
        assert nodes[2]["text"] == "italic"
        assert nodes[2]["marks"] == [{"type": "italic"}]

    def test_mixed_plain_and_bold(self):
        doc = markdown_to_doc("start **bold** end")
        nodes = _nodes(doc, 1)
        assert nodes[0]["text"] == "start "
        assert nodes[1]["text"] == "bold"
        assert nodes[1]["marks"] == [{"type": "bold"}]
        assert nodes[2]["text"] == " end"


# ---------------------------------------------------------------------------
# markdown_to_doc — block elements
# ---------------------------------------------------------------------------


class TestBlockElements:
    def test_heading_renders_as_bold_paragraph(self):
        doc = markdown_to_doc("# Title")
        nodes = _nodes(doc, 1)
        assert nodes[0]["marks"] == [{"type": "bold"}]
        assert nodes[0]["text"] == "Title"

    def test_unordered_list_item(self):
        doc = markdown_to_doc("- Item one")
        nodes = _nodes(doc, 1)
        assert nodes[0]["text"] == "• "
        assert nodes[1]["text"] == "Item one"

    def test_ordered_list_item(self):
        doc = markdown_to_doc("1. First")
        nodes = _nodes(doc, 1)
        assert nodes[0]["text"] == "1. "
        assert nodes[1]["text"] == "First"

    def test_multiple_list_items_produce_multiple_paragraphs(self):
        doc = markdown_to_doc("- A\n- B\n- C")
        assert len(_paragraphs(doc)) == 3

    def test_literal_backslash_n_converted_to_newline(self):
        doc = markdown_to_doc(r"line1\nline2")
        node = _text_node(doc, 1, 1)
        assert "\n" in node["text"]


# ---------------------------------------------------------------------------
# markdown_to_doc — validation errors
# ---------------------------------------------------------------------------


class TestValidationErrors:
    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            markdown_to_doc("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            markdown_to_doc("   \n\t  ")

    def test_error_message_exact(self):
        with pytest.raises(ValueError) as exc_info:
            markdown_to_doc("")
        assert str(exc_info.value) == (
            "Note body cannot be empty"
            " - at least one paragraph with content is required"
        )


# ---------------------------------------------------------------------------
# markdown_to_note_payload — envelope
# ---------------------------------------------------------------------------


class TestNotePayloadEnvelope:
    def test_required_envelope_fields(self):
        payload = markdown_to_note_payload("Hello")
        assert payload["tabId"] == "for-you"
        assert payload["surface"] == "feed"
        assert payload["replyMinimumRole"] == "everyone"

    def test_body_json_is_doc(self):
        payload = markdown_to_note_payload("Hello")
        assert payload["bodyJson"]["type"] == "doc"

    def test_no_attachment_ids_by_default(self):
        payload = markdown_to_note_payload("Hello")
        assert "attachmentIds" not in payload

    def test_attachment_ids_included_when_provided(self):
        payload = markdown_to_note_payload("Hello", attachment_ids=["uuid-1", "uuid-2"])
        assert payload["attachmentIds"] == ["uuid-1", "uuid-2"]

    def test_empty_attachment_ids_not_included(self):
        payload = markdown_to_note_payload("Hello", attachment_ids=[])
        assert "attachmentIds" not in payload

    def test_propagates_value_error_from_doc(self):
        with pytest.raises(ValueError):
            markdown_to_note_payload("")
