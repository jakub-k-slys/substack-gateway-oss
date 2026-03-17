from __future__ import annotations

from gateway_oss.client.base import SubstackHTTPBase

_API_PREFIX = "api/v1"


class PublicationClient(SubstackHTTPBase):
    """HTTP client scoped to a single Substack publication.

    Handles all requests to ``{publication_url}/api/v1/*``.
    Domain logic lives in the service classes (``gateway_oss.services.*``).
    """

    def __init__(
        self,
        substack_sid: str,
        connect_sid: str,
        publication_url: str,
        request_id: str | None = None,
    ) -> None:
        super().__init__(substack_sid, connect_sid, request_id)
        self._base = f"{publication_url.rstrip('/')}/{_API_PREFIX}"
