from __future__ import annotations

import pytest
from fastmcp import FastMCP

from gateway_drafts_mcp import _register

_TOKEN_SENTENCE = "The `token` argument is optional"
_DOC = (
    "https://github.com/jakub-k-slys/substack-gateway-oss/blob/main/"
    "docs/drafts-markdown.md"
)


async def _description(name: str) -> str:
    mcp = FastMCP("descriptions")
    _register(mcp)
    tool = await mcp.get_tool(name)
    assert tool is not None
    return tool.description or ""


@pytest.mark.anyio
async def test_update_draft_description_mentions_dialect_and_conflicts() -> None:
    description = await _description("update_draft")

    assert "::button" in description
    assert "substack-node" in description
    assert "expected_updated_at" in description


@pytest.mark.anyio
@pytest.mark.parametrize("name", ["get_draft", "create_draft", "update_draft"])
async def test_draft_body_tools_keep_token_sentence_and_point_to_docs(
    name: str,
) -> None:
    description = await _description(name)

    assert _TOKEN_SENTENCE in description
    assert _DOC in description
    assert "::defaults{align=left|center|right|justify|default}" in description
    assert ":::align" in description
    assert ":::callout" in description
    assert "{size=normal|large|full}" in description
    assert "{watermark=N%}" in description


@pytest.mark.anyio
@pytest.mark.parametrize("name", ["get_draft", "update_draft"])
async def test_read_and_update_descriptions_explain_updated_at_round_trip(
    name: str,
) -> None:
    description = await _description(name)

    assert "updated_at" in description
    assert "expected_updated_at" in description
