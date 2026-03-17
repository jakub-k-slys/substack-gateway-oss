from __future__ import annotations

# Register Pro step definitions when Behave is run from the workspace root:
#
#   uv run behave
#
# Importing these modules causes Behave to register their @given/@when/@then
# decorators into the active root step registry.
from packages.gateway_pro.features.steps.draft_body_converter import *  # noqa: F401, F403
from packages.gateway_pro.features.steps.drafts import *  # noqa: F401, F403
from packages.gateway_pro.features.steps.mcp_drafts import *  # noqa: F401, F403
from packages.gateway_pro.features.steps.oauth_flow import *  # noqa: F401, F403
from packages.gateway_pro.features.steps.oauth_provider import *  # noqa: F401, F403
