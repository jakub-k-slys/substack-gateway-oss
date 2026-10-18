"""Watermarking of draft images through Substack's ``image/watermark`` endpoint."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlsplit

from gateway_core.client.publication import PublicationClient

Position = Literal["top-right", "top-left", "bottom-right", "bottom-left"]

_SIZE_IN_NAME = re.compile(r"_(\d+)x(\d+)\.[A-Za-z0-9]+$")


@dataclass(frozen=True)
class WatermarkSpec:
    scale: float = 0.06
    position: Position = "top-right"
    opacity: int = 65


def compute_geometry(
    width: int, height: int, spec: WatermarkSpec
) -> tuple[int, int, int]:
    """Return ``(offset_x, offset_y, size)`` for the square watermark overlay.

    Mirrors the web editor: the overlay is ``scale`` of the image width, kept
    ``0.4%`` of the width from the top/bottom edge and four pixels further from
    the left/right edge.
    """
    # Round away float noise (0.06 * 1000 == 60.00000000000001) before ceil.
    size = math.ceil(round(spec.scale * width, 6))
    offset_y = round(0.004 * width)
    offset_x = offset_y + 4
    x = width - size - offset_x if spec.position.endswith("right") else offset_x
    y = height - size - offset_y if spec.position.startswith("bottom") else offset_y
    return x, y, size


def image_dimensions_from_url(url: str) -> tuple[int, int] | None:
    """Parse the ``_<W>x<H>.<ext>`` suffix Substack puts on hosted image names."""
    match = _SIZE_IN_NAME.search(urlsplit(url).path)
    if match is None:
        return None
    return int(match.group(1)), int(match.group(2))


class WatermarkService:
    def __init__(self, pub: PublicationClient) -> None:
        self._pub = pub

    async def apply(
        self, original_url: str, width: int, height: int, spec: WatermarkSpec
    ) -> str:
        """Overlay the publication logo on ``original_url``; return the new URL."""
        offset_x, offset_y, size = compute_geometry(width, height, spec)
        response = await self._pub.post(
            "image/watermark",
            json={
                "image": original_url,
                "offsetX": offset_x,
                "offsetY": offset_y,
                "width": size,
                "height": size,
                "opacity": spec.opacity,
            },
        )
        return str(response.json()["url"])
