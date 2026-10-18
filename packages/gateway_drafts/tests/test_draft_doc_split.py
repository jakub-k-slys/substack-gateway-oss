from __future__ import annotations

import json

from gateway_drafts.converters.markdown import (
    draft_body_to_markdown,
    markdown_to_draft_body,
    markdown_to_draft_doc,
)


def test_doc_is_a_dict_with_doc_type() -> None:
    doc = markdown_to_draft_doc("Hello")
    assert isinstance(doc, dict)
    assert doc["type"] == "doc"
    assert doc["content"][0]["type"] == "paragraph"


def test_body_is_json_dump_of_doc() -> None:
    markdown = "# Title\n\nPlain text"
    assert markdown_to_draft_body(markdown) == json.dumps(
        markdown_to_draft_doc(markdown), ensure_ascii=False
    )


def test_literal_backslash_n_in_single_line_input_is_expanded() -> None:
    # Agents often send JSON-escaped newlines; single-line input has its
    # literal "\n" escapes expanded to line breaks before parsing.
    doc = markdown_to_draft_doc("# Title\\n\\nBody text")
    assert [node["type"] for node in doc["content"]] == ["heading", "paragraph"]


def test_literal_backslash_n_in_multi_line_input_is_kept() -> None:
    doc = markdown_to_draft_doc("$$\n\\neg x\n$$")
    assert doc["content"][0]["attrs"]["persistentExpression"] == "\\neg x"


def test_one_paragraph_with_literal_backslash_n_round_trips_unchanged() -> None:
    doc = {
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "attrs": {"textAlign": None},
                "content": [
                    {"type": "text", "text": "use "},
                    {"type": "text", "text": "\\n", "marks": [{"type": "code"}]},
                    {"type": "text", "text": " or a\\nb"},
                ],
            }
        ],
    }
    markdown = draft_body_to_markdown(json.dumps(doc))
    assert markdown.endswith("\n")
    assert markdown_to_draft_doc(markdown) == doc


def test_draft_markdown_always_ends_with_a_newline() -> None:
    assert draft_body_to_markdown(markdown_to_draft_body("Hello")) == "Hello\n"
