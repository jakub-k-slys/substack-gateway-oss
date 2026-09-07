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
