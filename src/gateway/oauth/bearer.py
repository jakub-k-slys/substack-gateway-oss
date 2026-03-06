from __future__ import annotations

import base64
import json

from mcp.server.auth.provider import RefreshToken


class _RefreshTokenWithJti(RefreshToken):
    """RefreshToken extended with access_jti for cascade revocation."""

    access_jti: str | None = None


def _encode_bearer(substack_sid: str, connect_sid: str) -> str:
    """Encode Substack cookie values into the base64 bearer token format."""
    payload = {"substack_sid": substack_sid, "connect_sid": connect_sid}
    return base64.b64encode(json.dumps(payload).encode()).decode()


def _validate_bearer(bearer: str) -> None:
    """Raise ValueError if the bearer token cannot be decoded correctly."""
    try:
        decoded = json.loads(base64.b64decode(bearer.encode()))
    except Exception as exc:
        raise ValueError("Could not decode bearer token.") from exc
    for field in ("substack_sid", "connect_sid"):
        if not decoded.get(field):
            raise ValueError(f"Missing required field: {field}")
