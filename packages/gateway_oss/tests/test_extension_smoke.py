from __future__ import annotations

import importlib.metadata

import pytest

from gateway_oss.config import settings
from gateway_oss.extensions.base import GatewayExtensionContext

_GROUP = "substack_gateway_oss.extensions"


def _installed():
    return list(importlib.metadata.entry_points(group=_GROUP))


@pytest.mark.skipif(not _installed(), reason="no downstream extensions installed")
def test_installed_extensions_load() -> None:
    """Każde zainstalowane rozszerzenie ładuje się i nie rzuca na get_module_info."""
    ctx = GatewayExtensionContext(settings=settings)
    for ep in _installed():
        obj = ep.load()
        ext = obj() if callable(obj) else obj
        assert getattr(ext, "name", None)
        ext.get_module_info(ctx)  # nie może rzucać (importuje ścieżki gateway_oss.*)


def test_full_app_boots() -> None:
    """Pełna apka wstaje, a root '/' raportuje moduł gateway-oss (+ każdy zainstalowany)."""
    from starlette.testclient import TestClient

    from gateway_oss import create_app

    with TestClient(create_app()) as client:
        body = client.get("/").json()
    names = {m["name"] for m in body["modules"]}
    assert "gateway-oss" in names
    # jeśli zainstalowane są rozszerzenia, muszą pojawić się dodatkowe moduły
    if _installed():
        assert len(names) > 1
