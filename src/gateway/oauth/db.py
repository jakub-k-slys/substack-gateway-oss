from __future__ import annotations

import contextlib
import hashlib
import secrets
from collections.abc import AsyncIterator
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Double, Integer, NullPool, Text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


# ---------------------------------------------------------------------------
# ORM models
# ---------------------------------------------------------------------------


class Base(DeclarativeBase):
    pass


class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )


class DBOAuthClient(Base):
    __tablename__ = "oauth_clients"

    client_id: Mapped[str] = mapped_column(Text, primary_key=True)
    client_data: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )


class DBAuthRequest(Base):
    __tablename__ = "auth_requests"

    request_id: Mapped[str] = mapped_column(Text, primary_key=True)
    client_id: Mapped[str] = mapped_column(Text, nullable=False)
    code_challenge: Mapped[str] = mapped_column(Text, nullable=False)
    redirect_uri: Mapped[str] = mapped_column(Text, nullable=False)
    redirect_uri_provided_explicitly: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    scopes: Mapped[str] = mapped_column(Text, nullable=False)
    state: Mapped[str | None] = mapped_column(Text)
    resource: Mapped[str | None] = mapped_column(Text)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )


class DBLoginSession(Base):
    __tablename__ = "login_sessions"

    session_id: Mapped[str] = mapped_column(Text, primary_key=True)
    request_id: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )


class DBUserCredential(Base):
    __tablename__ = "user_credentials"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bearer: Mapped[str] = mapped_column(Text, nullable=False)
    pub_url: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class DBAuthCode(Base):
    __tablename__ = "auth_codes"

    code: Mapped[str] = mapped_column(Text, primary_key=True)
    client_id: Mapped[str] = mapped_column(Text, nullable=False)
    redirect_uri: Mapped[str] = mapped_column(Text, nullable=False)
    redirect_uri_provided_explicitly: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )
    scopes: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[float] = mapped_column(Double, nullable=False)
    code_challenge: Mapped[str] = mapped_column(Text, nullable=False)
    resource: Mapped[str | None] = mapped_column(Text)
    user_id: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )


class DBAccessToken(Base):
    __tablename__ = "access_tokens"

    jti: Mapped[str] = mapped_column(Text, primary_key=True)
    client_id: Mapped[str] = mapped_column(Text, nullable=False)
    scopes: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[int] = mapped_column(Integer, nullable=False)
    revoked: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false", default=False
    )
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )


class DBRefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token_hash: Mapped[str] = mapped_column(Text, primary_key=True)
    client_id: Mapped[str] = mapped_column(Text, nullable=False)
    scopes: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[int | None] = mapped_column(Integer)
    revoked: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false", default=False
    )
    access_jti: Mapped[str | None] = mapped_column(Text)
    user_id: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )


# ---------------------------------------------------------------------------
# Engine and session
# ---------------------------------------------------------------------------


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        from gateway.config import settings

        if not settings.database_url:
            raise RuntimeError("DATABASE_URL is not configured")
        _engine = create_async_engine(settings.database_url, poolclass=NullPool)
    return _engine


def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(get_engine(), expire_on_commit=False)
    return _session_factory


@contextlib.asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    """Yield an ORM session that auto-commits on success and rolls back on error."""
    async with _get_session_factory().begin() as session:
        yield session


# ---------------------------------------------------------------------------
# Schema management
# ---------------------------------------------------------------------------


async def init_db() -> None:
    """Create all tables and run migrations. Idempotent."""
    from gateway.config import settings

    if not settings.database_url:
        return
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ---------------------------------------------------------------------------
# Token helpers
# ---------------------------------------------------------------------------


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def generate_opaque_token() -> str:
    return secrets.token_urlsafe(48)
