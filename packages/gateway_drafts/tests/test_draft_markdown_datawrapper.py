from __future__ import annotations

import json

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
    body = json.dumps(
        {
            "type": "doc",
            "content": [
                {
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
            ],
        }
    )
    assert draft_body_to_markdown(body) == (
        "```datawrapper\nhttps://datawrapper.dwcdn.net/boimj/2/\n```"
    )
