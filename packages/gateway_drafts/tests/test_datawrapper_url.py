from __future__ import annotations

import pytest

from gateway_drafts.converters.draft_body_resolver import _normalize_datawrapper_url

RESOLVE = "https://www.datawrapper.de/_/boimj/"


@pytest.mark.parametrize(
    "url",
    [
        "https://www.datawrapper.de/_/boimj/",
        "https://www.datawrapper.de/_/boimj",
        "https://datawrapper.dwcdn.net/boimj/2/",
        "https://datawrapper.dwcdn.net/boimj/",
    ],
)
def test_known_forms_normalize_to_resolve_url(url: str) -> None:
    assert _normalize_datawrapper_url(url) == RESOLVE


def test_unparseable_url_raises() -> None:
    with pytest.raises(ValueError):
        _normalize_datawrapper_url("https://example.com/not-a-chart")
