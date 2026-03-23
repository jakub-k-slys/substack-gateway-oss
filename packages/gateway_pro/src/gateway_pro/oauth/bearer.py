from __future__ import annotations

import base64
import json

from mcp.server.auth.provider import RefreshToken


class _RefreshTokenWithJti(RefreshToken):
    """RefreshToken extended with access_jti for cascade revocation and user_id propagation."""

    access_jti: str | None = None
    user_id: int | None = None


def validate_bearer(bearer: str) -> None:
    """Raise ValueError if the bearer token cannot be decoded correctly."""
    try:
        decoded = json.loads(base64.b64decode(bearer.encode()))
    except Exception as exc:
        raise ValueError("Could not decode bearer token.") from exc
    for field in ("publication_url", "substack_sid", "connect_sid"):
        if not decoded.get(field):
            raise ValueError(f"Missing required field: {field}")
