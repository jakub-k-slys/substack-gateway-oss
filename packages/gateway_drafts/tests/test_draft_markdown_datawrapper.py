from __future__ import annotations

import json

import pytest

from gateway_drafts.converters.dialect.errors import DraftMarkdownError
from gateway_drafts.converters.markdown import (
    draft_body_to_markdown,
    markdown_to_draft_body,
)


def _nodes(markdown: str) -> list[dict]:
    return json.loads(markdown_to_draft_body(markdown))["content"]


def test_datawrapper_fence_becomes_placeholder() -> None:
    nodes = _nodes("```datawrapper\nhttps://www.datawrapper.de/_/boimj/\n```")
    assert nodes == [
        {
            "type": "_unresolved_datawrapper",
            "attrs": {"url": "https://www.datawrapper.de/_/boimj/"},
        }
    ]


def test_plain_code_fence_is_unaffected() -> None:
    nodes = _nodes("```python\nprint(1)\n```")
    assert nodes[0]["type"] == "highlighted_code_block"


def test_datawrapper_node_round_trips_to_fence() -> None:
    # A stored datawrapper node carries thumbnails and metadata the
    # ```datawrapper fence cannot express, so it is written verbatim as a
    # substack-node fence and parses back to the very same node.
    node = {
        "type": "datawrapper",
        "attrs": {
            "url": "https://datawrapper.dwcdn.net/boimj/2/",
            "thumbnail_url": "https://s3/x.png",
            "thumbnail_url_full": "https://s3/x-full.png",
            "height": 400,
            "title": "T",
            "description": "",
        },
    }
    body = json.dumps({"type": "doc", "content": [node]})
    markdown = draft_body_to_markdown(body)
    assert markdown == (
        "```substack-node\n"
        + json.dumps(node, indent=2, ensure_ascii=False)
        + "\n```\n"
    )
    assert _nodes(markdown) == [node]


@pytest.mark.parametrize(
    "body",
    [
        "https://app.datawrapper.de/chart/AbC12/visualize",
        "https://example.com/not-a-chart",
        "",
        "https://www.datawrapper.de/_/boimj/ https://www.datawrapper.de/_/other/",
    ],
)
def test_bad_datawrapper_fence_is_a_markdown_error_at_its_line(body: str) -> None:
    lines = ["Intro.", "", "```datawrapper", *([body] if body else []), "```"]
    markdown = "\n".join(lines)
    with pytest.raises(DraftMarkdownError) as exc:
        markdown_to_draft_body(markdown)
    assert exc.value.line == 3
    assert "Datawrapper" in exc.value.message


def test_whitespace_around_datawrapper_url_is_ignored() -> None:
    nodes = _nodes("```datawrapper\n  https://datawrapper.dwcdn.net/boimj/2/  \n\n```")
    assert nodes[0]["attrs"]["url"] == "https://datawrapper.dwcdn.net/boimj/2/"
