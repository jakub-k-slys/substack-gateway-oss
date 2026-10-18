"""Golden round-trip tests for the draft Markdown façade.

``web_editor_draft.json`` is a synthetic doc in the shape Substack's web editor
sends (every node kind from the capture, invented content).
``gateway_draft.json`` is what ``markdown_to_draft_doc`` produces for a dialect
sample with no placeholders. Both must survive doc → Markdown → doc unchanged,
and their Markdown must be a fixed point of Markdown → doc → Markdown.
``legacy_gateway_draft.json`` is what an older gateway stored (paragraphs and
headings without ``textAlign``); it reads back without fences and with only
that default filled in.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from gateway_drafts.converters.markdown import (
    draft_body_to_markdown,
    markdown_to_draft_body,
    markdown_to_draft_doc,
)

FIXTURES = Path(__file__).parent / "fixtures"
NAMES = ["web_editor_draft.json", "gateway_draft.json"]


def _canon(d: Any) -> str:
    return json.dumps(d, sort_keys=True, ensure_ascii=False)


@pytest.mark.parametrize("name", NAMES)
def test_doc_round_trip_is_lossless(name: str) -> None:
    doc = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert _canon(markdown_to_draft_doc(draft_body_to_markdown(json.dumps(doc)))) == (
        _canon(doc)
    )


@pytest.mark.parametrize("name", NAMES)
def test_markdown_is_idempotent(name: str) -> None:
    md1 = draft_body_to_markdown((FIXTURES / name).read_text(encoding="utf-8"))
    md2 = draft_body_to_markdown(markdown_to_draft_body(md1))
    assert md1 == md2


def _with_text_align(node: Any) -> Any:
    """Fill the default ``textAlign`` on legacy paragraphs and headings."""
    if isinstance(node, list):
        return [_with_text_align(item) for item in node]
    if not isinstance(node, dict):
        return node
    out = {key: _with_text_align(value) for key, value in node.items()}
    if out.get("type") in ("paragraph", "heading"):
        out["attrs"] = {"textAlign": None, **(out.get("attrs") or {})}
    return out


def test_legacy_draft_reads_back_without_fences() -> None:
    body = (FIXTURES / "legacy_gateway_draft.json").read_text(encoding="utf-8")
    markdown = draft_body_to_markdown(body)
    assert "substack-node" not in markdown
    assert _canon(markdown_to_draft_doc(markdown)) == _canon(
        _with_text_align(json.loads(body))
    )
    assert draft_body_to_markdown(markdown_to_draft_body(markdown)) == markdown
