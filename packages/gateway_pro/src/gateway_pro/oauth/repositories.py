"""Repository classes for OAuth database access.

Each repository is instantiated with an AsyncSession and exposes
domain-oriented methods. All SQL stays here; callers never import
SQLAlchemy directly.
"""

from __future__ import annotations

import types

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from gateway_pro.oauth.db import (
    DBAccessToken,
    DBAuthCode,
    DBAuthRequest,
    DBLoginSession,
    DBOAuthClient,
    DBRefreshToken,
    DBUser,
    get_session,
)


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_by_email(self, email: str) -> DBUser | None:
        result = await self._s.execute(select(DBUser).where(DBUser.email == email))
        return result.scalar_one_or_none()

    async def save(self, user: DBUser) -> None:
        self._s.add(user)

    async def delete_by_email(self, email: str) -> bool:
        result = await self._s.execute(
            delete(DBUser).where(DBUser.email == email).returning(DBUser.id)
        )
        return result.fetchone() is not None


class OAuthClientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get(self, client_id: str) -> DBOAuthClient | None:
        return await self._s.get(DBOAuthClient, client_id)

    async def upsert(self, client_id: str, client_data: str) -> None:
        stmt = pg_insert(DBOAuthClient).values(
            client_id=client_id, client_data=client_data
        )
        await self._s.execute(
            stmt.on_conflict_do_update(
                index_elements=["client_id"],
                set_={"client_data": stmt.excluded.client_data},
            )
        )


class AuthRequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get(self, request_id: str) -> DBAuthRequest | None:
        return await self._s.get(DBAuthRequest, request_id)

    async def save(self, auth_request: DBAuthRequest) -> None:
        self._s.add(auth_request)

    async def delete(self, request_id: str) -> None:
        await self._s.execute(
            delete(DBAuthRequest).where(DBAuthRequest.request_id == request_id)
        )


class LoginSessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get(self, session_id: str) -> DBLoginSession | None:
        return await self._s.get(DBLoginSession, session_id)

    async def save(self, login_session: DBLoginSession) -> None:
        self._s.add(login_session)

    async def delete(self, session_id: str) -> None:
        await self._s.execute(
            delete(DBLoginSession).where(DBLoginSession.session_id == session_id)
        )


class AuthCodeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get(self, code: str, client_id: str) -> DBAuthCode | None:
        result = await self._s.execute(
            select(DBAuthCode).where(
                (DBAuthCode.code == code) & (DBAuthCode.client_id == client_id)
            )
        )
        return result.scalar_one_or_none()

    async def save(self, auth_code: DBAuthCode) -> None:
        self._s.add(auth_code)

    async def consume(self, code: str) -> int | None:
        """Atomically delete the code and return its user_id, or None if already used."""
        result = await self._s.execute(
            delete(DBAuthCode)
            .where(DBAuthCode.code == code)
            .returning(DBAuthCode.user_id)
        )
        row = result.fetchone()
        return row[0] if row is not None else None


class AccessTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get(self, jti: str) -> DBAccessToken | None:
        return await self._s.get(DBAccessToken, jti)

    async def save(self, token: DBAccessToken) -> None:
        self._s.add(token)

    async def revoke(self, jti: str) -> None:
        await self._s.execute(
            update(DBAccessToken).where(DBAccessToken.jti == jti).values(revoked=True)
        )


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get(self, token_hash: str) -> DBRefreshToken | None:
        return await self._s.get(DBRefreshToken, token_hash)

    async def get_active(
        self, token_hash: str, client_id: str
    ) -> DBRefreshToken | None:
        result = await self._s.execute(
            select(DBRefreshToken).where(
                (DBRefreshToken.token_hash == token_hash)
                & (DBRefreshToken.client_id == client_id)
                & (DBRefreshToken.revoked.is_(False))
            )
        )
        return result.scalar_one_or_none()

    async def save(self, token: DBRefreshToken) -> None:
        self._s.add(token)

    async def revoke(self, token_hash: str) -> None:
        await self._s.execute(
            update(DBRefreshToken)
            .where(DBRefreshToken.token_hash == token_hash)
            .values(revoked=True)
        )


class UnitOfWork:
    """Single session shared across all repositories; commits on success, rolls back on error."""

    users: UserRepository
    oauth_clients: OAuthClientRepository
    auth_requests: AuthRequestRepository
    login_sessions: LoginSessionRepository
    auth_codes: AuthCodeRepository
    access_tokens: AccessTokenRepository
    refresh_tokens: RefreshTokenRepository

    async def __aenter__(self) -> UnitOfWork:
        self._cm = get_session()
        session = await self._cm.__aenter__()
        self.users = UserRepository(session)
        self.oauth_clients = OAuthClientRepository(session)
        self.auth_requests = AuthRequestRepository(session)
        self.login_sessions = LoginSessionRepository(session)
        self.auth_codes = AuthCodeRepository(session)
        self.access_tokens = AccessTokenRepository(session)
        self.refresh_tokens = RefreshTokenRepository(session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        return await self._cm.__aexit__(exc_type, exc_val, exc_tb)
