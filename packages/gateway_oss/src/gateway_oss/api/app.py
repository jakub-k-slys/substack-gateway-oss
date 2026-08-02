from __future__ import annotations

# Backward-compatibility shim: the FastAPI instance is assembled in the shell
# package. A downstream extension imports `from gateway_oss.api.app import api`.
from substack_gateway.api_app import api  # noqa: F401

__all__ = ["api"]
