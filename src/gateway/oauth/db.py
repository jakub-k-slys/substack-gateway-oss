from __future__ import annotations

import hashlib
import secrets
from typing import TYPE_CHECKING

from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

if TYPE_CHECKING:
    pass

_engine: AsyncEngine | None = None

_CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id              SERIAL PRIMARY KEY,
        email           TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        created_at      TIMESTAMPTZ DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS oauth_clients (
        client_id   TEXT PRIMARY KEY,
        client_data TEXT NOT NULL,
        created_at  TIMESTAMPTZ DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS auth_requests (
        request_id                       TEXT PRIMARY KEY,
        client_id                        TEXT NOT NULL,
        code_challenge                   TEXT NOT NULL,
        redirect_uri                     TEXT NOT NULL,
        redirect_uri_provided_explicitly BOOLEAN NOT NULL,
        scopes                           TEXT NOT NULL,
        state                            TEXT,
        resource                         TEXT,
        expires_at                       TIMESTAMPTZ NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS auth_codes (
        code                             TEXT PRIMARY KEY,
        client_id                        TEXT NOT NULL,
        redirect_uri                     TEXT NOT NULL,
        redirect_uri_provided_explicitly BOOLEAN NOT NULL,
        scopes                           TEXT NOT NULL,
        expires_at                       DOUBLE PRECISION NOT NULL,
        code_challenge                   TEXT NOT NULL,
        resource                         TEXT,
        created_at                       TIMESTAMPTZ DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS access_tokens (
        jti         TEXT PRIMARY KEY,
        client_id   TEXT NOT NULL,
        scopes      TEXT NOT NULL,
        expires_at  INTEGER NOT NULL,
        revoked     BOOLEAN DEFAULT FALSE,
        created_at  TIMESTAMPTZ DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS refresh_tokens (
        token_hash  TEXT PRIMARY KEY,
        client_id   TEXT NOT NULL,
        scopes      TEXT NOT NULL,
        expires_at  INTEGER,
        revoked     BOOLEAN DEFAULT FALSE,
        access_jti  TEXT,
        created_at  TIMESTAMPTZ DEFAULT NOW()
    )
    """,
]


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        from gateway.config import settings

        if not settings.database_url:
            raise RuntimeError("DATABASE_URL is not configured")
        _engine = create_async_engine(settings.database_url, poolclass=NullPool)
    return _engine


async def init_db() -> None:
    """Create all tables if they don't exist. Idempotent."""
    from gateway.config import settings

    if not settings.database_url:
        return
    async with get_engine().begin() as conn:
        for stmt in _CREATE_TABLES:
            await conn.execute(text(stmt))


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def generate_opaque_token() -> str:
    return secrets.token_urlsafe(48)
