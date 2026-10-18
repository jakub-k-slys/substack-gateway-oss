from __future__ import annotations

import json

from gateway_drafts.converters.markdown import (
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


def test_literal_backslash_n_in_single_line_input_stays_text() -> None:
    # The old converter expanded a literal "\n" in single-line input into a
    # line break. That rewrote text the serializer writes on one line (e.g. a
    # paragraph mentioning "\n"), so the façade now passes input through as is.
    doc = markdown_to_draft_doc("first\\nsecond")
    assert doc["content"] == [
        {
            "type": "paragraph",
            "attrs": {"textAlign": None},
            "content": [{"type": "text", "text": "first\\nsecond"}],
        }
    ]
