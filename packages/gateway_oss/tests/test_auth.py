from __future__ import annotations

import base64
import json

import pytest

from gateway_oss.auth import decode_bearer_credentials


def _encode(payload: dict[str, str]) -> str:
    return base64.b64encode(json.dumps(payload).encode()).decode()


def test_decode_bearer_credentials_accepts_publication_url() -> None:
    credentials = decode_bearer_credentials(
        _encode(
            {
                "publication_url": "https://example.substack.com",
                "substack_sid": "sid",
                "connect_sid": "csid",
            }
        )
    )

    assert credentials.publication_url == "https://example.substack.com"
    assert credentials.substack_sid == "sid"
    assert credentials.connect_sid == "csid"


def test_decode_bearer_credentials_requires_publication_url() -> None:
    with pytest.raises(ValueError, match="publication_url"):
        decode_bearer_credentials(
            _encode({"substack_sid": "sid", "connect_sid": "csid"})
        )


def test_decode_bearer_credentials_rejects_invalid_publication_url() -> None:
    with pytest.raises(ValueError, match="valid HTTP or HTTPS publication_url"):
        decode_bearer_credentials(
            _encode(
                {
                    "publication_url": "notaurl",
                    "substack_sid": "sid",
                    "connect_sid": "csid",
                }
            )
        )
