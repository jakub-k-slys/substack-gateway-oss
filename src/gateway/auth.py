from __future__ import annotations

import base64

from pydantic import ValidationError

from gateway.models.schemas import BearerCredentials


def decode_bearer_credentials(raw: str) -> BearerCredentials:
    """Decode a base64-encoded JSON Bearer token into BearerCredentials.

    Args:
        raw: Token string with any ``"Bearer "`` prefix already stripped.

    Raises:
        ValueError: If the token is not valid base64-encoded JSON credentials,
            or if ``substack_sid`` / ``connect_sid`` are absent.
    """
    try:
        decoded = base64.b64decode(raw).decode()
        credentials = BearerCredentials.model_validate_json(decoded)
    except (ValidationError, Exception) as exc:
        raise ValueError(
            "Invalid token: expected base64-encoded JSON credentials"
        ) from exc
    if not credentials.substack_sid or not credentials.connect_sid:
        raise ValueError("Token must contain substack_sid and connect_sid")
    return credentials
