from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from gateway_core.auth import BearerCredentials

_MESSAGE = (
    "No Substack credentials. Pass `token` with base64-encoded credentials, "
    "or run a deployment that resolves credentials from the authenticated "
    "session."
)


class MissingCredentialsError(RuntimeError):
    """Raised when a call carries no usable Substack credentials."""

    def __init__(self, message: str = _MESSAGE) -> None:
        super().__init__(message)


@runtime_checkable
class CredentialResolver(Protocol):
    """Resolves the credentials of an already-authenticated caller.

    Implementations map a caller's identity to the Substack credentials stored
    for them. Returning ``None`` means the caller is not known, which the
    caller of this protocol reports as :class:`MissingCredentialsError`.
    """

    async def resolve(self, access_token: Any) -> BearerCredentials | None:
        """Return credentials for ``access_token``'s subject, or ``None``.

        ``access_token`` is the transport's authenticated token object — in
        practice, an instance of ``fastmcp.server.auth.AccessToken``, or
        ``None`` when the request carried no authentication. It is typed
        loosely so this package stays free of that dependency.

        Implementations MUST treat ``None`` as unauthenticated and return
        ``None`` for it rather than serving any stored credential set — a
        resolver that ignores the distinction would hand one caller's
        credentials to every anonymous request.
        """


_resolver: CredentialResolver | None = None


def set_credential_resolver(resolver: CredentialResolver | None) -> None:
    """Install the process-wide resolver. Pass ``None`` to clear it."""
    global _resolver
    _resolver = resolver


def get_credential_resolver() -> CredentialResolver | None:
    """Return the installed resolver, or ``None`` when none is installed."""
    return _resolver
