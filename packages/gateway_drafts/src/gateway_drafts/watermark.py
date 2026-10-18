"""Watermarking of draft images through Substack's ``image/watermark`` endpoint."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlsplit

from gateway_core.client.exceptions import SubstackAPIError
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
    the left/right edge. The square is clamped to fit the image: at least one
    pixel, never larger than the shorter side, and never placed outside it
    (e.g. ``watermark=100%`` or a tiny image).
    """
    # Round away float noise (0.06 * 1000 == 60.00000000000001) before ceil.
    size = math.ceil(round(spec.scale * width, 6))
    size = max(1, min(size, width, height))
    offset_y = round(0.004 * width)
    offset_x = offset_y + 4
    x = width - size - offset_x if spec.position.endswith("right") else offset_x
    y = height - size - offset_y if spec.position.startswith("bottom") else offset_y
    return _clamp(x, width - size), _clamp(y, height - size), size


def _clamp(offset: int, limit: int) -> int:
    return max(0, min(offset, limit))


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
        try:
            data = response.json()
        except ValueError:  # not JSON (json.JSONDecodeError is a ValueError)
            data = None
        url = data.get("url") if isinstance(data, dict) else None
        if not isinstance(url, str) or not url:
            raise SubstackAPIError(
                502, f"Substack's watermark endpoint returned no URL for {original_url}"
            )
        return url
