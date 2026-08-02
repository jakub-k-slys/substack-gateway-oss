from __future__ import annotations

# Temporary re-export shim: extension discovery now lives in the shell package.
# Removed once the assembly modules are relocated (see plan Task 2).
from substack_gateway.ext_loader import (  # noqa: F401
    DISABLE_ENTRYPOINTS_ENV_VAR,
    ENTRYPOINT_GROUP,
    ENV_VAR,
    load_extensions,
)
