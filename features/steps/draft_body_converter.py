from __future__ import annotations

import json
import textwrap

from behave import then, when

from converters.markdown import draft_body_to_markdown, markdown_to_draft_body


@when('I convert draft markdown "{markdown}"')
def step_convert_draft_inline(context, markdown):
    body_str = markdown_to_draft_body(markdown)
    context.draft_body_str = body_str
    context.draft_doc = json.loads(body_str)
    context.current_list_node = None
    context.current_code_block = None
    context.current_quote_node = None


@when("I convert draft markdown:")
def step_convert_draft_docstring(context):
    markdown = textwrap.dedent(context.text).strip()
    body_str = markdown_to_draft_body(markdown)
    context.draft_body_str = body_str
    context.draft_doc = json.loads(body_str)
    context.current_list_node = None
    context.current_code_block = None
    context.current_quote_node = None


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _nodes(context) -> list:
    return context.draft_doc["content"]


def _node(context, idx: int) -> dict:
    nodes = _nodes(context)
    assert len(nodes) >= idx, f"Expected at least {idx} node(s), got {len(nodes)}"
    return nodes[idx - 1]


def _para_node(context, para_idx: int, node_idx: int) -> dict:
    para = _node(context, para_idx)
    assert para["type"] == "paragraph", (
        f"Node {para_idx} is not a paragraph: {para['type']}"
    )
    content = para["content"]
    assert len(content) >= node_idx, (
        f"Paragraph {para_idx}: expected at least {node_idx} text node(s), got {len(content)}"
    )
    return content[node_idx - 1]


# ------------------------------------------------------------------
# Doc-level assertions
# ------------------------------------------------------------------


@then("the draft body is a JSON string")
def step_draft_body_is_json(context):
    assert isinstance(context.draft_body_str, str), "draft body is not a string"
    json.loads(context.draft_body_str)  # raises if invalid JSON


@then('the draft doc type is "{doc_type}"')
def step_draft_doc_type(context, doc_type):
    assert context.draft_doc["type"] == doc_type, (
        f"Expected type {doc_type!r}, got {context.draft_doc['type']!r}"
    )


@then("the draft doc has no schema version attribute")
def step_draft_doc_no_schema_version(context):
    attrs = context.draft_doc.get("attrs", {})
    assert "schemaVersion" not in attrs, (
        f"Expected no schemaVersion but found: {attrs.get('schemaVersion')}"
    )


@then("the draft doc has {count:d} node")
def step_draft_node_count_singular(context, count):
    step_draft_node_count_plural(context, count)


@then("the draft doc has {count:d} nodes")
def step_draft_node_count_plural(context, count):
    actual = len(_nodes(context))
    assert actual == count, f"Expected {count} node(s), got {actual}: {_nodes(context)}"


# ------------------------------------------------------------------
# Node type assertions
# ------------------------------------------------------------------


@then("draft node {idx:d} is a paragraph")
def step_draft_node_is_paragraph(context, idx):
    node = _node(context, idx)
    assert node["type"] == "paragraph", f"Expected paragraph, got {node['type']}"


@then('draft node {idx:d} is a paragraph with {count:d} text node "{text}"')
def step_draft_node_is_paragraph_with_text(context, idx, count, text):
    node = _node(context, idx)
    assert node["type"] == "paragraph", f"Expected paragraph, got {node['type']}"
    content = node["content"]
    assert len(content) == count, f"Expected {count} text node(s), got {len(content)}"
    assert content[0]["text"] == text, f"Expected {text!r}, got {content[0]['text']!r}"


@then('draft node {idx:d} is a heading with level {level:d} and text "{text}"')
def step_draft_node_is_heading(context, idx, level, text):
    node = _node(context, idx)
    assert node["type"] == "heading", f"Expected heading, got {node['type']}"
    actual_level = node["attrs"]["level"]
    assert actual_level == level, f"Expected level {level}, got {actual_level}"
    actual_text = "".join(n["text"] for n in node["content"])
    assert actual_text == text, f"Expected {text!r}, got {actual_text!r}"


@then('draft node {idx:d} is a highlighted_code_block with language "{lang}"')
def step_draft_node_is_code_block_with_lang(context, idx, lang):
    node = _node(context, idx)
    assert node["type"] == "highlighted_code_block", (
        f"Expected highlighted_code_block, got {node['type']}"
    )
    actual_lang = (node.get("attrs") or {}).get("language")
    assert actual_lang == lang, f"Expected language {lang!r}, got {actual_lang!r}"
    context.current_code_block = node


@then("draft node {idx:d} is a highlighted_code_block with null language")
def step_draft_node_is_code_block_null_lang(context, idx):
    node = _node(context, idx)
    assert node["type"] == "highlighted_code_block", (
        f"Expected highlighted_code_block, got {node['type']}"
    )
    actual_lang = (node.get("attrs") or {}).get("language")
    assert actual_lang is None, f"Expected null language, got {actual_lang!r}"
    context.current_code_block = node


@then('draft code block text contains "{text}"')
def step_draft_code_block_text_contains(context, text):
    node = context.current_code_block
    assert node is not None, (
        "No current code block — use a highlighted_code_block step first"
    )
    content_text = "".join(n.get("text", "") for n in node.get("content", []))
    assert text in content_text, (
        f"Expected {text!r} in code block, got {content_text!r}"
    )


@then("draft node {idx:d} is a blockquote with {count:d} inner node")
def step_draft_node_is_blockquote_singular(context, idx, count):
    step_draft_node_is_blockquote_plural(context, idx, count)


@then("draft node {idx:d} is a blockquote with {count:d} inner nodes")
def step_draft_node_is_blockquote_plural(context, idx, count):
    node = _node(context, idx)
    assert node["type"] == "blockquote", f"Expected blockquote, got {node['type']}"
    actual = len(node.get("content", []))
    assert actual == count, f"Expected {count} inner node(s), got {actual}"
    context.current_quote_node = node


@then('draft blockquote inner node {idx:d} is a paragraph with text "{text}"')
def step_draft_blockquote_inner_node(context, idx, text):
    node = context.current_quote_node
    assert node is not None, "No current quote node — use a blockquote step first"
    inner = node.get("content", [])
    assert len(inner) >= idx, f"Expected at least {idx} inner node(s), got {len(inner)}"
    para = inner[idx - 1]
    assert para["type"] == "paragraph", f"Expected paragraph, got {para['type']}"
    actual = "".join(n.get("text", "") for n in para.get("content", []))
    assert actual == text, f"Expected {text!r}, got {actual!r}"


@then("draft node {idx:d} is a pullquote with {count:d} inner node")
def step_draft_node_is_pullquote_singular(context, idx, count):
    step_draft_node_is_pullquote_plural(context, idx, count)


@then("draft node {idx:d} is a pullquote with {count:d} inner nodes")
def step_draft_node_is_pullquote_plural(context, idx, count):
    node = _node(context, idx)
    assert node["type"] == "pullquote", f"Expected pullquote, got {node['type']}"
    actual = len(node.get("content", []))
    assert actual == count, f"Expected {count} inner node(s), got {actual}"
    context.current_quote_node = node


@then('draft pullquote inner node {idx:d} is a paragraph with text "{text}"')
def step_draft_pullquote_inner_node(context, idx, text):
    node = context.current_quote_node
    assert node is not None, "No current quote node — use a pullquote step first"
    inner = node.get("content", [])
    assert len(inner) >= idx, f"Expected at least {idx} inner node(s), got {len(inner)}"
    para = inner[idx - 1]
    assert para["type"] == "paragraph", f"Expected paragraph, got {para['type']}"
    actual = "".join(n.get("text", "") for n in para.get("content", []))
    assert actual == text, f"Expected {text!r}, got {actual!r}"


@then(
    'draft paragraph {para:d} text node {node_idx:d} is a link with text "{text}" and href "{href}"'
)
def step_draft_para_node_link(context, para, node_idx, text, href):
    n = _para_node(context, para, node_idx)
    assert n["text"] == text, f"Expected text {text!r}, got {n['text']!r}"
    marks = {m["type"] for m in n.get("marks", [])}
    assert "link" in marks, f"Expected link mark, got {marks}"
    link_attrs = next(
        m.get("attrs") or {} for m in n.get("marks", []) if m["type"] == "link"
    )
    actual_href = link_attrs.get("href", "")
    assert actual_href == href, f"Expected href {href!r}, got {actual_href!r}"


@then("draft node {idx:d} is a bullet_list with {count:d} items")
def step_draft_node_is_bullet_list(context, idx, count):
    node = _node(context, idx)
    assert node["type"] == "bullet_list", f"Expected bullet_list, got {node['type']}"
    actual = len(node["content"])
    assert actual == count, f"Expected {count} item(s), got {actual}"
    context.current_list_node = node


@then("draft node {idx:d} is an ordered_list with {count:d} items")
def step_draft_node_is_ordered_list(context, idx, count):
    node = _node(context, idx)
    assert node["type"] == "ordered_list", f"Expected ordered_list, got {node['type']}"
    actual = len(node["content"])
    assert actual == count, f"Expected {count} item(s), got {actual}"
    context.current_list_node = node


# ------------------------------------------------------------------
# List assertions
# ------------------------------------------------------------------


@then("draft ordered_list start attr is {start:d}")
def step_draft_ordered_list_start(context, start):
    node = context.current_list_node
    assert node is not None, "No current list node — use a list-type step first"
    actual = node["attrs"]["start"]
    assert actual == start, f"Expected start={start}, got {actual}"


@then('draft list item {idx:d} text is "{text}"')
def step_draft_list_item_text(context, idx, text):
    node = context.current_list_node
    assert node is not None, "No current list node — use a list-type step first"
    item = node["content"][idx - 1]
    assert item["type"] == "list_item", f"Expected list_item, got {item['type']}"
    para = item["content"][0]
    assert para["type"] == "paragraph", (
        f"Expected paragraph inside list_item, got {para['type']}"
    )
    actual = "".join(n["text"] for n in para["content"])
    assert actual == text, f"Expected {text!r}, got {actual!r}"


# ------------------------------------------------------------------
# Inline text node assertions
# ------------------------------------------------------------------


@then('draft paragraph {para:d} text node {node_idx:d} is plain "{text}"')
def step_draft_para_node_plain(context, para, node_idx, text):
    n = _para_node(context, para, node_idx)
    assert n["text"] == text, f"Expected {text!r}, got {n['text']!r}"
    assert "marks" not in n, f"Expected no marks, got {n.get('marks')}"


@then(
    'draft paragraph {para:d} text node {node_idx:d} has mark "{mark}" and text "{text}"'
)
def step_draft_para_node_single_mark(context, para, node_idx, mark, text):
    n = _para_node(context, para, node_idx)
    assert n["text"] == text, f"Expected {text!r}, got {n['text']!r}"
    actual_marks = [m["type"] for m in n.get("marks", [])]
    assert mark in actual_marks, f"Expected mark {mark!r} in {actual_marks}"


@then(
    'draft paragraph {para:d} text node {node_idx:d} has marks "{marks_str}" and text "{text}"'
)
def step_draft_para_node_multi_mark(context, para, node_idx, marks_str, text):
    n = _para_node(context, para, node_idx)
    assert n["text"] == text, f"Expected {text!r}, got {n['text']!r}"
    expected = set(marks_str.split(","))
    actual = {m["type"] for m in n.get("marks", [])}
    assert expected == actual, f"Expected marks {expected}, got {actual}"


# ------------------------------------------------------------------
# Reverse converter steps
# ------------------------------------------------------------------


@then('the draft body round-trips to markdown "{expected}"')
def step_round_trip_inline(context, expected):
    result = draft_body_to_markdown(context.draft_body_str)
    assert result == expected, f"Expected {expected!r}, got {result!r}"


@then("the draft body round-trips to markdown:")
def step_round_trip_docstring(context):
    expected = textwrap.dedent(context.text).strip()
    result = draft_body_to_markdown(context.draft_body_str)
    assert result == expected, f"Expected {expected!r}, got {result!r}"


@when("I reverse-convert the draft body JSON:")
def step_reverse_convert_docstring(context):
    body_json = textwrap.dedent(context.text).strip()
    context.reverse_result = draft_body_to_markdown(body_json)


@then('the markdown result is "{expected}"')
def step_markdown_result(context, expected):
    assert context.reverse_result == expected, (
        f"Expected {expected!r}, got {context.reverse_result!r}"
    )
