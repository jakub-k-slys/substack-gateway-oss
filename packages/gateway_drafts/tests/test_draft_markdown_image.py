from __future__ import annotations

import json

from gateway_drafts.converters.markdown import (
    draft_body_to_markdown,
    markdown_to_draft_body,
)


def _nodes(markdown: str) -> list[dict]:
    return json.loads(markdown_to_draft_body(markdown))["content"]


def test_image_line_becomes_placeholder() -> None:
    nodes = _nodes("![A cat](https://x/cat.png)")
    assert nodes == [
        {
            "type": "_unresolved_image",
            "attrs": {"src": "https://x/cat.png", "alt": "A cat"},
        }
    ]


def test_data_uri_image_is_parsed_whole() -> None:
    nodes = _nodes("![](data:image/png;base64,QUJDRA==)")
    assert nodes[0]["type"] == "_unresolved_image"
    assert nodes[0]["attrs"]["src"] == "data:image/png;base64,QUJDRA=="
    assert nodes[0]["attrs"]["alt"] == ""


def test_captioned_image_node_round_trips() -> None:
    body = json.dumps(
        {
            "type": "doc",
            "content": [
                {
                    "type": "captionedImage",
                    "content": [
                        {
                            "type": "image2",
                            "attrs": {
                                "src": "https://s3/cat.png",
                                "alt": "A cat",
                                "width": 10,
                                "height": 10,
                            },
                        }
                    ],
                }
            ],
        }
    )
    assert draft_body_to_markdown(body) == "![A cat](https://s3/cat.png)"


def test_captioned_image_with_null_alt_round_trips() -> None:
    body = json.dumps(
        {
            "type": "doc",
            "content": [
                {
                    "type": "captionedImage",
                    "content": [
                        {
                            "type": "image2",
                            "attrs": {"src": "https://s3/x.png", "alt": None},
                        }
                    ],
                }
            ],
        }
    )
    assert draft_body_to_markdown(body) == "![](https://s3/x.png)"
