from __future__ import annotations

import textwrap

from behave import then, when

from converters.markdown import markdown_to_note_payload


@when('I convert the markdown "{markdown}"')
def step_convert_inline(context, markdown):
    context.convert_error = None
    try:
        context.payload = markdown_to_note_payload(markdown)
    except ValueError as exc:
        context.convert_error = exc
        context.payload = None


@when("I convert the markdown:")
def step_convert_docstring(context):
    context.convert_error = None
    # Behave puts the docstring in context.text; dedent to remove feature indentation.
    markdown = textwrap.dedent(context.text).strip()
    try:
        context.payload = markdown_to_note_payload(markdown)
    except ValueError as exc:
        context.convert_error = exc
        context.payload = None


@when("I convert the markdown with an empty list item")
def step_convert_empty_list_item(context):
    # Middle item is "- " (dash + space, no content) — mirrors the TS test.
    markdown = "- First item\n- \n- Third item"
    context.convert_error = None
    try:
        context.payload = markdown_to_note_payload(markdown)
    except ValueError as exc:
        context.convert_error = exc
        context.payload = None


@when("I convert the markdown with literal backslash-n escapes")
def step_convert_literal_newlines(context):
    # Raw string: \n is backslash+n (2 chars), not a newline character.
    markdown = r"First line\nSecond line\n\nThird paragraph"
    context.convert_error = None
    try:
        context.payload = markdown_to_note_payload(markdown)
    except ValueError as exc:
        context.convert_error = exc
        context.payload = None


@when("I convert the whitespace-only markdown")
def step_convert_whitespace(context):
    context.convert_error = None
    try:
        context.payload = markdown_to_note_payload("   \n\t  ")
    except ValueError as exc:
        context.convert_error = exc
        context.payload = None


@when("I convert the empty markdown")
def step_convert_empty(context):
    context.convert_error = None
    try:
        context.payload = markdown_to_note_payload("")
    except ValueError as exc:
        context.convert_error = exc
        context.payload = None


# ------------------------------------------------------------------
# Payload envelope assertions
# ------------------------------------------------------------------


@then('the note payload tabId is "{value}"')
def step_tab_id(context, value):
    assert context.payload["tabId"] == value, context.payload["tabId"]


@then('the note payload surface is "{value}"')
def step_surface(context, value):
    assert context.payload["surface"] == value, context.payload["surface"]


@then('the note payload replyMinimumRole is "{value}"')
def step_reply_role(context, value):
    assert context.payload["replyMinimumRole"] == value


@then('the note payload bodyJson type is "{value}"')
def step_body_type(context, value):
    assert context.payload["bodyJson"]["type"] == value


@then('the note payload bodyJson schemaVersion is "{value}"')
def step_body_schema(context, value):
    assert context.payload["bodyJson"]["attrs"]["schemaVersion"] == value


# ------------------------------------------------------------------
# Paragraph / text node assertions
# ------------------------------------------------------------------


def _paragraphs(context) -> list:
    return context.payload["bodyJson"]["content"]


def _node(context, para_idx: int, node_idx: int) -> dict:
    paragraphs = _paragraphs(context)
    assert len(paragraphs) >= para_idx, (
        f"Expected at least {para_idx} paragraph(s), got {len(paragraphs)}"
    )
    paragraph = paragraphs[para_idx - 1]
    nodes = paragraph["content"]
    assert len(nodes) >= node_idx, (
        f"Paragraph {para_idx}: expected at least {node_idx} node(s), got {len(nodes)}"
    )
    return nodes[node_idx - 1]


@then("the note payload has {count:d} paragraph")
def step_paragraph_count_singular(context, count):
    step_paragraph_count_plural(context, count)


@then("the note payload has {count:d} paragraphs")
def step_paragraph_count_plural(context, count):
    actual = len(_paragraphs(context))
    assert actual == count, f"Expected {count} paragraph(s), got {actual}"


@then('paragraph {para:d} has {count:d} text node with text "{text}"')
def step_single_node_plain(context, para, count, text):
    paragraphs = _paragraphs(context)
    nodes = paragraphs[para - 1]["content"]
    assert len(nodes) == count, f"Expected {count} node(s), got {len(nodes)}: {nodes}"
    assert nodes[0]["text"] == text, f"Expected {text!r}, got {nodes[0]['text']!r}"
    assert "marks" not in nodes[0], f"Expected no marks, got {nodes[0].get('marks')}"


@then('paragraph {para:d} has {count:d} text node with bold text "{text}"')
def step_single_node_bold(context, para, count, text):
    paragraphs = _paragraphs(context)
    nodes = paragraphs[para - 1]["content"]
    assert len(nodes) == count, f"Expected {count} node(s), got {len(nodes)}: {nodes}"
    assert nodes[0]["text"] == text, f"Expected {text!r}, got {nodes[0]['text']!r}"
    marks = nodes[0].get("marks", [])
    assert marks == [{"type": "bold"}], f"Expected bold marks, got {marks}"


@then('paragraph {para:d} has 1 text node with bold and italic text "{text}"')
def step_single_node_bold_italic(context, para, text):
    paragraphs = _paragraphs(context)
    nodes = paragraphs[para - 1]["content"]
    assert len(nodes) == 1, f"Expected 1 node, got {len(nodes)}: {nodes}"
    assert nodes[0]["text"] == text, f"Expected {text!r}, got {nodes[0]['text']!r}"
    mark_types = {m["type"] for m in nodes[0].get("marks", [])}
    assert mark_types == {"bold", "italic"}, (
        f"Expected bold+italic marks, got {mark_types}"
    )


@then('paragraph {para:d} text node {node:d} is plain "{text}"')
def step_node_plain(context, para, node, text):
    n = _node(context, para, node)
    assert n["text"] == text, f"Expected {text!r}, got {n['text']!r}"
    assert "marks" not in n, f"Expected no marks, got {n.get('marks')}"


@then('paragraph {para:d} text node {node:d} is bold "{text}"')
def step_node_bold(context, para, node, text):
    n = _node(context, para, node)
    assert n["text"] == text, f"Expected {text!r}, got {n['text']!r}"
    assert n.get("marks") == [{"type": "bold"}], f"Expected bold, got {n.get('marks')}"


@then('paragraph {para:d} text node {node:d} is italic "{text}"')
def step_node_italic(context, para, node, text):
    n = _node(context, para, node)
    assert n["text"] == text, f"Expected {text!r}, got {n['text']!r}"
    assert n.get("marks") == [{"type": "italic"}], (
        f"Expected italic, got {n.get('marks')}"
    )


@then("paragraph {para:d} has 1 text node containing a newline")
def step_single_node_has_newline(context, para):
    paragraphs = _paragraphs(context)
    nodes = paragraphs[para - 1]["content"]
    assert len(nodes) == 1, f"Expected 1 node, got {len(nodes)}"
    assert "\n" in nodes[0]["text"], (
        f"Expected newline in text, got {nodes[0]['text']!r}"
    )


@then('paragraph {para:d} text node {node:d} is code "{text}"')
def step_node_code(context, para, node, text):
    n = _node(context, para, node)
    assert n["text"] == text, f"Expected {text!r}, got {n['text']!r}"
    assert n.get("marks") == [{"type": "code"}], f"Expected code, got {n.get('marks')}"


# ------------------------------------------------------------------
# Error assertions
# ------------------------------------------------------------------


@then('a ValueError is raised with message "{message}"')
def step_error_raised(context, message):
    assert context.convert_error is not None, (
        "Expected a ValueError but none was raised"
    )
    actual = str(context.convert_error)
    assert actual == message, f"Expected {message!r}, got {actual!r}"
