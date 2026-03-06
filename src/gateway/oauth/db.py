from __future__ import annotations

import hashlib
import secrets

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Double,
    Integer,
    MetaData,
    NullPool,
    Table,
    Text,
    text,
)
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

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
    # login_sessions holds the intermediate state between phase-1 (email/password)
    # and phase-2 (Substack bearer token) of the login flow.
    """
    CREATE TABLE IF NOT EXISTS login_sessions (
        session_id  TEXT PRIMARY KEY,
        request_id  TEXT NOT NULL,
        user_id     INTEGER NOT NULL,
        expires_at  TIMESTAMPTZ NOT NULL
    )
    """,
    # user_credentials stores the Substack bearer token and publication URL
    # that each user provides during phase-2 login.  These are used by the
    # MCP tool dependencies instead of per-request HTTP headers.
    """
    CREATE TABLE IF NOT EXISTS user_credentials (
        user_id     INTEGER PRIMARY KEY,
        bearer      TEXT NOT NULL,
        pub_url     TEXT NOT NULL,
        updated_at  TIMESTAMPTZ DEFAULT NOW()
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
        user_id                          INTEGER,
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

# Migration: add columns that are new in this version but may be absent on
# existing deployments (CREATE TABLE IF NOT EXISTS won't add them).
_MIGRATIONS = [
    "ALTER TABLE auth_codes ADD COLUMN IF NOT EXISTS user_id INTEGER",
]

# ---------------------------------------------------------------------------
# SQLAlchemy table definitions (used for typed DML expressions)
# ---------------------------------------------------------------------------

metadata = MetaData()

t_users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", Text, unique=True, nullable=False),
    Column("hashed_password", Text, nullable=False),
    Column("created_at", DateTime(timezone=True)),
)

t_oauth_clients = Table(
    "oauth_clients",
    metadata,
    Column("client_id", Text, primary_key=True),
    Column("client_data", Text, nullable=False),
    Column("created_at", DateTime(timezone=True)),
)

t_auth_requests = Table(
    "auth_requests",
    metadata,
    Column("request_id", Text, primary_key=True),
    Column("client_id", Text, nullable=False),
    Column("code_challenge", Text, nullable=False),
    Column("redirect_uri", Text, nullable=False),
    Column("redirect_uri_provided_explicitly", Boolean, nullable=False),
    Column("scopes", Text, nullable=False),
    Column("state", Text),
    Column("resource", Text),
    Column("expires_at", DateTime(timezone=True), nullable=False),
)

t_login_sessions = Table(
    "login_sessions",
    metadata,
    Column("session_id", Text, primary_key=True),
    Column("request_id", Text, nullable=False),
    Column("user_id", Integer, nullable=False),
    Column("expires_at", DateTime(timezone=True), nullable=False),
)

t_user_credentials = Table(
    "user_credentials",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("bearer", Text, nullable=False),
    Column("pub_url", Text, nullable=False),
    Column("updated_at", DateTime(timezone=True)),
)

t_auth_codes = Table(
    "auth_codes",
    metadata,
    Column("code", Text, primary_key=True),
    Column("client_id", Text, nullable=False),
    Column("redirect_uri", Text, nullable=False),
    Column("redirect_uri_provided_explicitly", Boolean, nullable=False),
    Column("scopes", Text, nullable=False),
    Column("expires_at", Double, nullable=False),
    Column("code_challenge", Text, nullable=False),
    Column("resource", Text),
    Column("user_id", Integer),
    Column("created_at", DateTime(timezone=True)),
)

t_access_tokens = Table(
    "access_tokens",
    metadata,
    Column("jti", Text, primary_key=True),
    Column("client_id", Text, nullable=False),
    Column("scopes", Text, nullable=False),
    Column("expires_at", Integer, nullable=False),
    Column("revoked", Boolean),
    Column("created_at", DateTime(timezone=True)),
)

t_refresh_tokens = Table(
    "refresh_tokens",
    metadata,
    Column("token_hash", Text, primary_key=True),
    Column("client_id", Text, nullable=False),
    Column("scopes", Text, nullable=False),
    Column("expires_at", Integer),
    Column("revoked", Boolean),
    Column("access_jti", Text),
    Column("created_at", DateTime(timezone=True)),
)


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        from gateway.config import settings

        if not settings.database_url:
            raise RuntimeError("DATABASE_URL is not configured")
        _engine = create_async_engine(settings.database_url, poolclass=NullPool)
    return _engine


async def init_db() -> None:
    """Create all tables and run migrations. Idempotent."""
    from gateway.config import settings

    if not settings.database_url:
        return
    async with get_engine().begin() as conn:
        for stmt in _CREATE_TABLES:
            await conn.execute(text(stmt))
        for stmt in _MIGRATIONS:
            await conn.execute(text(stmt))


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def generate_opaque_token() -> str:
    return secrets.token_urlsafe(48)
