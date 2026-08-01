from __future__ import annotations


class SubstackAuthError(Exception):
    """Raised when Substack returns 401 or 403."""

    def __init__(
        self,
        status_code: int = 401,
        message: str = "Invalid or expired Substack session token",
    ) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(message)


class SubstackAPIError(Exception):
    """Raised for other Substack API errors (network failures, 5xx, etc.)."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"Substack API error {status_code}: {message}")
