from __future__ import annotations

import logging

import bcrypt
from fastapi import APIRouter, HTTPException, Query
from gateway_oss.config import settings
from pydantic import BaseModel

from gateway_pro.oauth.db import DBUser, init_db
from gateway_pro.oauth.repositories import UnitOfWork

router = APIRouter(tags=["users"])

_log = logging.getLogger(__name__)


class CreateUserRequest(BaseModel):
    email: str
    password: str


class DeleteUserRequest(BaseModel):
    email: str


@router.post("/users", status_code=201)
async def create_user(
    body: CreateUserRequest,
    token: str = Query(...),
) -> dict[str, str]:
    """Create a gateway user (OAuth login credentials). Requires ?token."""
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Invalid token.")

    if not settings.oauth_enabled:
        raise HTTPException(
            status_code=503, detail="OAuth is not configured on this server."
        )

    await init_db()

    hashed = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()
    email = body.email.strip().lower()

    try:
        async with UnitOfWork() as uow:
            await uow.users.save(DBUser(email=email, hashed_password=hashed))
    except Exception as exc:
        if "unique" in str(exc).lower():
            raise HTTPException(
                status_code=409, detail="A user with that email already exists."
            ) from exc
        _log.exception("Failed to create user")
        raise HTTPException(status_code=500, detail="Failed to create user.") from exc

    return {"email": email}


@router.delete("/users", status_code=204)
async def delete_user(
    body: DeleteUserRequest,
    token: str = Query(...),
) -> None:
    """Delete a gateway user by email. Requires ?token (admin token)."""
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Invalid token.")

    if not settings.oauth_enabled:
        raise HTTPException(
            status_code=503, detail="OAuth is not configured on this server."
        )

    await init_db()

    email = body.email.strip().lower()

    async with UnitOfWork() as uow:
        deleted = await uow.users.delete_by_email(email)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found.")
