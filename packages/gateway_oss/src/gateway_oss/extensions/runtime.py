from __future__ import annotations

# Temporary re-export shim: GatewayRuntime/get_runtime now live in the shell
# package. Removed once the assembly modules are relocated (see plan Task 2).
from substack_gateway.runtime import (  # noqa: F401
    GatewayRuntime,
    _single_provider,
    get_runtime,
)
