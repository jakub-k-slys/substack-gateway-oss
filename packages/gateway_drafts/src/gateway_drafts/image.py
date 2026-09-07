from __future__ import annotations

import base64
import logging

from gateway_core.client.publication import PublicationClient
from gateway_drafts.schemas import ImageUploadResult

_log = logging.getLogger(__name__)


def data_uri(content_type: str, raw: bytes) -> str:
    """Build a ``data:<mime>;base64,<…>`` URI for Substack's image field."""
    return f"data:{content_type};base64,{base64.b64encode(raw).decode()}"


class ImagesService:
    """Uploads images to Substack's publication image endpoint.

    ``POST /api/v1/image`` accepts a data URI or a URL in the ``image`` field
    and re-hosts it on Substack's S3, returning the canonical URL and pixel
    dimensions the ``image2`` node needs.
    """

    def __init__(self, pub: PublicationClient) -> None:
        self._pub = pub

    async def upload(self, image: str) -> ImageUploadResult:
        _log.debug("Uploading image (%d chars)", len(image))
        r = await self._pub.post("image", json={"image": image})
        return ImageUploadResult.from_substack(r.json())
