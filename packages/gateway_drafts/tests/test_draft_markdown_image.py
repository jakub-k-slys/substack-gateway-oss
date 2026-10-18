from __future__ import annotations

import json

from _dialect_helpers import doc_with_image

from gateway_drafts.converters.dialect.attrs import fill_defaults
from gateway_drafts.converters.markdown import (
    draft_body_to_markdown,
    markdown_to_draft_body,
)

_HOSTED = "https://substack-post-media.s3.amazonaws.com/public/images/cat_10x10.png"


def _nodes(markdown: str) -> list[dict]:
    return json.loads(markdown_to_draft_body(markdown))["content"]


def test_external_image_line_becomes_placeholder() -> None:
    nodes = _nodes("![A cat](https://x/cat.png)")
    assert nodes == [
        {
            "type": "_unresolved_image",
            "attrs": {
                "src": "https://x/cat.png",
                "alt": "A cat",
                "image_attrs": {},
                "watermark": None,
            },
        }
    ]


def test_hosted_image_line_becomes_captioned_image_directly() -> None:
    nodes = _nodes(f"![A cat]({_HOSTED})")
    attrs = fill_defaults("image2", {"src": _HOSTED, "alt": "A cat"})
    assert nodes == [
        {"type": "captionedImage", "content": [{"type": "image2", "attrs": attrs}]}
    ]


def test_data_uri_image_is_parsed_whole() -> None:
    nodes = _nodes("![](data:image/png;base64,QUJDRA==)")
    assert nodes[0]["type"] == "_unresolved_image"
    assert nodes[0]["attrs"]["src"] == "data:image/png;base64,QUJDRA=="
    assert nodes[0]["attrs"]["alt"] == ""


def test_captioned_image_node_round_trips() -> None:
    body = json.dumps(doc_with_image(src=_HOSTED, alt="A cat", width=10, height=10))
    markdown = draft_body_to_markdown(body)
    assert markdown == f"![A cat]({_HOSTED}){{height=10 width=10}}"
    assert json.loads(markdown_to_draft_body(markdown)) == json.loads(body)


def test_captioned_image_with_null_alt_round_trips() -> None:
    body = json.dumps(doc_with_image(src=_HOSTED, alt=None))
    assert draft_body_to_markdown(body) == f"![]({_HOSTED})"


def test_image_markdown_cannot_reproduce_falls_back_to_a_verbatim_fence() -> None:
    # An image2 missing most of its attributes (or hosted elsewhere) cannot be
    # written as ![alt](src) without changing the node, so it is kept verbatim.
    image = {
        "type": "captionedImage",
        "content": [{"type": "image2", "attrs": {"src": "https://s3/x.png"}}],
    }
    body = json.dumps({"type": "doc", "content": [image]})
    markdown = draft_body_to_markdown(body)
    assert markdown.startswith("```substack-node\n")
    assert _nodes(markdown) == [image]
