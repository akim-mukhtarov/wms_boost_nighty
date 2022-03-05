from typing import Tuple, Optional, Dict
from datetime import timedelta
from jose import jwt

from app.models import User
from app.utils import get_db
from sqlalchemy.orm import Session
from fastapi import Security, HTTPException, Depends
from fastapi_jwt import (
    JwtAccessBearer,
    JwtRefreshBearer,
    JwtAuthorizationCredentials
)


secret_key = "secret_key"
# Read access token from bearer header only
access_security = JwtAccessBearer(
    secret_key=secret_key,
    auto_error=True,
    access_expires_delta=timedelta(hours=12)  # change access token validation timedelta
)


refresh_security = JwtRefreshBearer(
    secret_key=secret_key,
    auto_error=True  # automatically raise HTTPException: HTTP_401_UNAUTHORIZED
)


def raw_decode(token: str) -> Optional[Dict]:
    return jwt.decode(
            token,
            secret_key,
            algorithms=jwt.ALGORITHMS.HS256,
            options={"leeway": 10})


def create_access_token(sub) -> str:
    return access_security.create_access_token(subject=sub)


def create_refresh_token(sub) -> str:
    return refresh_security.create_refresh_token(subject=sub)


def create_tokens(user: User) -> Tuple[str]:
    sub = { 'id': user.id }
    access_token = create_access_token(sub)
    refresh_token = create_refresh_token(sub)
    return access_token, refresh_token


def get_current_user(
        sub: JwtAuthorizationCredentials = Security(access_security),
        db: Session = Depends(get_db)
) -> User:
    user_id = sub["id"]
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(401)
    return user
