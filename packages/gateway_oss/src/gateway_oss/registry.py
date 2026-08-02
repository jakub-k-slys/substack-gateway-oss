from __future__ import annotations

# Temporary re-export shim: the capability registry now lives in the shell
# package. Removed once the assembly modules are relocated (see plan Task 2).
from substack_gateway.registry import (  # noqa: F401
    CAPABILITY_GROUP,
    load_mcp_capabilities,
    load_rest_capabilities,
)
