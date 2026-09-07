from __future__ import annotations

import base64


class InvalidCursorError(ValueError):
    """Raised when a paging cursor cannot be decoded."""


def encode_offset(offset: int) -> str:
    return base64.urlsafe_b64encode(f"o:{offset}".encode()).decode().rstrip("=")


def decode_offset(cursor: str) -> int:
    try:
        pad = "=" * (-len(cursor) % 4)
        raw = base64.urlsafe_b64decode(cursor + pad).decode()
    except (ValueError, UnicodeDecodeError) as exc:
        raise InvalidCursorError("invalid cursor") from exc
    if not raw.startswith("o:"):
        raise InvalidCursorError("invalid cursor")
    try:
        offset = int(raw[2:])
    except ValueError as exc:
        raise InvalidCursorError("invalid cursor") from exc
    if offset < 0:
        raise InvalidCursorError("invalid cursor")
    return offset
