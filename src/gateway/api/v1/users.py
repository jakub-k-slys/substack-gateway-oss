from __future__ import annotations

import logging

import bcrypt
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from gateway.oauth.db import DBUser, get_session, init_db

router = APIRouter(tags=["users"])

_log = logging.getLogger(__name__)

_INIT_TOKEN = (
    "WW91IHNoYWxsIG5vdCBwYXNzLiBZb3Ugc2hhbGwgbm90IHBhc3MsIHlvdSBzaGFsbCBub3QgcGFzcyEK"
)


class CreateUserRequest(BaseModel):
    email: str
    password: str


@router.post("/users", status_code=201)
async def create_user(
    body: CreateUserRequest,
    token: str = Query(...),
) -> dict[str, str]:
    """Create a gateway user (OAuth login credentials). Requires ?token."""
    if token != _INIT_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token.")

    from gateway.config import settings

    if not settings.oauth_enabled:
        raise HTTPException(
            status_code=503, detail="OAuth is not configured on this server."
        )

    await init_db()

    hashed = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()
    email = body.email.strip().lower()

    try:
        async with get_session() as session:
            session.add(DBUser(email=email, hashed_password=hashed))
    except Exception as exc:
        if "unique" in str(exc).lower():
            raise HTTPException(
                status_code=409, detail="A user with that email already exists."
            ) from exc
        _log.exception("Failed to create user")
        raise HTTPException(status_code=500, detail="Failed to create user.") from exc

    return {"email": email}
