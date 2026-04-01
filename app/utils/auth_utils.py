from datetime import datetime, timedelta
from typing import Protocol, Any
from jose import JWTError, jwt
from pwdlib import PasswordHash
from app.core import settings
from fastapi.exceptions import HTTPException
from fastapi import status

from app.models.auth_model import User
password_hash = PasswordHash.recommended()


class AuthRepositoryLike(Protocol):
    async def get_user_by_username(self, username: str) -> Any:
        ...


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(req_password: str, hashed_password: str) -> bool:
    return password_hash.verify(req_password, hashed_password)


def create_token(data: dict, expires_delta: timedelta | None, type: str) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "type": type})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str, repo: AuthRepositoryLike) -> User:
    user = await repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist with this username")
    if not verify_password(req_password=password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def decode_token(refresh_token: str, expected_type) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate the refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.ALGORITHM])
        if payload.get("type") != expected_type:
            raise credentials_exception
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception
