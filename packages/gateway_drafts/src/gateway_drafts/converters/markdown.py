"""Draft Markdown ↔ Substack draft body: a thin façade over ``dialect``.

``markdown_to_draft_doc`` parses the draft dialect into a ProseMirror doc
(raising ``DraftMarkdownError`` on malformed dialect constructs);
``draft_body_to_markdown`` writes a stored draft body back as dialect Markdown,
losslessly: ``markdown_to_draft_doc(draft_body_to_markdown(body))`` gives back
the doc in ``body`` (with legacy paragraphs and headings given the default
``textAlign``).
"""

from __future__ import annotations

import json
from typing import Any

from gateway_drafts.converters.dialect.blocks import parse_blocks
from gateway_drafts.converters.dialect.serialize import serialize_doc


def markdown_to_draft_doc(markdown: str) -> dict[str, Any]:
    # Only expand literal ``\n`` escapes for single-line input (agents often
    # send JSON-escaped newlines). Multi-line input already carries real
    # newlines, and expanding there would corrupt LaTeX/escape sequences that
    # legitimately start with ``\n`` (``\neg``, ``\nabla``, ``\nu``).
    # ``draft_body_to_markdown`` output always ends with a newline, so it is
    # never expanded here.
    if "\n" not in markdown:
        markdown = markdown.replace("\\n", "\n")
    return {"type": "doc", "content": parse_blocks(markdown)}


def markdown_to_draft_body(markdown: str) -> str:
    return json.dumps(markdown_to_draft_doc(markdown), ensure_ascii=False)


def draft_body_to_markdown(body: str) -> str:
    # The trailing newline keeps the output multi-line, so feeding it back to
    # ``markdown_to_draft_doc`` never triggers the literal ``\n`` expansion.
    markdown = serialize_doc(json.loads(body))
    return f"{markdown}\n" if markdown else ""
