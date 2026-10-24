from __future__ import annotations

from types import SimpleNamespace

import pytest
import respx
from starlette.testclient import TestClient

from .steps.comment_engagement import *  # noqa: F403
from .steps.common import *  # noqa: F403
from .steps.draft_body_converter import *  # noqa: F403
from .steps.drafts import *  # noqa: F403
from .steps.health import *  # noqa: F403
from .steps.markdown_converter import *  # noqa: F403
from .steps.mcp_tools import *  # noqa: F403
from .steps.me import *  # noqa: F403
from .steps.note_engagement import *  # noqa: F403
from .steps.notes_create import *  # noqa: F403
from .steps.post_engagement import *  # noqa: F403
from .steps.post_stats import *  # noqa: F403
from .steps.posts import *  # noqa: F403
from .steps.profiles import *  # noqa: F403
from .steps.reader import *  # noqa: F403
from .steps.root import *  # noqa: F403
from .steps.stats import *  # noqa: F403

_BDD_SUBSTACK_MAX_CONNECTIONS = 100
_BDD_SUBSTACK_MAX_KEEPALIVE_CONNECTIONS = 100


@pytest.fixture(scope="session")
def app():
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("SUBSTACK_GATEWAY_DISABLE_ENTRYPOINT_EXTENSIONS", "1")
        # Imported here: importing the app modules already builds the runtime,
        # which loads the extensions, so the variable must be set by then.
        from gateway_oss import create_app

        return create_app()


@pytest.fixture
def context(app, monkeypatch):
    """Per-scenario state shared between steps."""
    from gateway_oss.config import settings

    monkeypatch.setattr(
        settings, "substack_max_connections", _BDD_SUBSTACK_MAX_CONNECTIONS
    )
    monkeypatch.setattr(
        settings,
        "substack_max_keepalive_connections",
        _BDD_SUBSTACK_MAX_KEEPALIVE_CONNECTIONS,
    )
    respx_mock = respx.mock(assert_all_mocked=True)
    respx_mock.start()
    yield SimpleNamespace(
        client=TestClient(app, raise_server_exceptions=False),
        headers={},
        response=None,
        mcp_result=None,
        mcp_error=None,
        respx_mock=respx_mock,
    )
    respx_mock.stop()
