"""Unit tests for gateway.oauth.db helper functions."""

from __future__ import annotations

import hashlib

import pytest

from gateway.oauth.db import generate_opaque_token, hash_token


class TestHashToken:
    def test_is_deterministic(self):
        assert hash_token("abc") == hash_token("abc")

    def test_produces_hex_sha256(self):
        result = hash_token("hello")
        expected = hashlib.sha256(b"hello").hexdigest()
        assert result == expected

    def test_different_inputs_produce_different_hashes(self):
        assert hash_token("token-a") != hash_token("token-b")

    def test_returns_64_char_hex_string(self):
        result = hash_token("any-token")
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)


class TestGenerateOpaqueToken:
    def test_returns_string(self):
        assert isinstance(generate_opaque_token(), str)

    def test_is_url_safe(self):
        token = generate_opaque_token()
        # url_safe base64 uses only A-Z a-z 0-9 - _
        assert all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" for c in token)

    def test_has_sufficient_entropy(self):
        # 48 bytes → ≥64 base64 chars
        assert len(generate_opaque_token()) >= 64

    def test_tokens_are_unique(self):
        tokens = {generate_opaque_token() for _ in range(20)}
        assert len(tokens) == 20


def test_init_db_noop_without_database_url(monkeypatch):
    """init_db should return without touching the engine when DATABASE_URL is unset."""
    import asyncio
    from unittest.mock import patch

    import gateway.oauth.db as db_module
    from gateway.config import settings

    monkeypatch.setattr(settings, "database_url", None)
    with patch.object(db_module, "get_engine") as mock_engine:
        asyncio.run(db_module.init_db())
        mock_engine.assert_not_called()
