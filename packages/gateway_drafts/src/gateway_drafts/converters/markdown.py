"""Draft Markdown ↔ Substack draft body: a thin façade over ``dialect``.

``markdown_to_draft_doc`` parses the draft dialect into a ProseMirror doc
(raising ``DraftMarkdownError`` on malformed dialect constructs);
``draft_body_to_markdown`` writes a stored draft body back as dialect Markdown,
losslessly: ``markdown_to_draft_doc(draft_body_to_markdown(body))`` gives back
the doc in ``body``.
"""

from __future__ import annotations

import json
from typing import Any

from gateway_drafts.converters.dialect.blocks import parse_blocks
from gateway_drafts.converters.dialect.serialize import serialize_doc


def markdown_to_draft_doc(markdown: str) -> dict[str, Any]:
    return {"type": "doc", "content": parse_blocks(markdown)}


def markdown_to_draft_body(markdown: str) -> str:
    return json.dumps(markdown_to_draft_doc(markdown), ensure_ascii=False)


def draft_body_to_markdown(body: str) -> str:
    return serialize_doc(json.loads(body))
