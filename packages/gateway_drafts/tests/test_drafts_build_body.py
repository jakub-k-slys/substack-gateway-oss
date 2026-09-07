from __future__ import annotations

import json
from typing import Any, cast

import pytest

from gateway_drafts.converters.markdown import markdown_to_draft_body
from gateway_drafts.service import DraftsService


def _strip_latex_ids(obj: object) -> object:
    """Recursively remove random 'id' keys from latex_block attrs so that
    two independently-generated docs can be compared for structural equality."""
    if isinstance(obj, dict):
        node_type = obj.get("type")
        result = {k: _strip_latex_ids(v) for k, v in obj.items()}
        if (
            node_type == "latex_block"
            and "attrs" in result
            and isinstance(result["attrs"], dict)
        ):
            result["attrs"] = {k: v for k, v in result["attrs"].items() if k != "id"}
        return result
    if isinstance(obj, list):
        return [_strip_latex_ids(item) for item in obj]
    return obj


@pytest.mark.anyio
async def test_build_body_matches_the_sync_converter() -> None:
    # No pub calls happen for plain markdown; None is a safe stand-in here.
    service = DraftsService(pub=cast(Any, None), sub=cast(Any, None))
    built = await service._build_body("# Title\n\n$$E = mc^2$$")
    expected = markdown_to_draft_body("# Title\n\n$$E = mc^2$$")
    assert _strip_latex_ids(json.loads(built)) == _strip_latex_ids(json.loads(expected))
