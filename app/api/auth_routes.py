from typing import Annotated, List
from fastapi import Depends, Request, Response, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas.token_schema import TokenResponse
from app.schemas.user_schema import UserResponse, UserSignUp, UserUpdate
from app.core import LoggerSetup
from app.services import AuthService
from app.repositories import AuthRepository
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core import settings
from datetime import timedelta
from app.utils.auth_utils import authenticate_user, create_token, verify_refresh_token
from fastapi.exceptions import HTTPException

logger = LoggerSetup.setup_logger(__name__)
auth_router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    logger.info("starting auth service")
    return AuthService(db)


@auth_router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(service: AuthService = Depends(get_service)):
    logger.info("getting all users")
    return await service.get_all_users()


@auth_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserSignUp, service: AuthService = Depends(get_service)):
    logger.info("creating user")
    return await service.create_user(data)


@auth_router.put("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(data: UserUpdate, id, service: AuthService = Depends(get_service)):
    logger.info("Update user")
    return await service.update_user(data, id)


@auth_router.post("/login", response_model=TokenResponse)
async def login(response: Response, data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    repo = AuthRepository(db)
    user = await authenticate_user(data.username, data.password, repo)

    access_ttl = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    refresh_ttl = timedelta(days=settings.REFRESH_TOKEN_EXPIRES)

    access_token = create_token({"sub": user.username}, access_ttl, type="access")
    refresh_token = create_token({"sub": user.username}, refresh_ttl, type="refresh")
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(refresh_ttl.total_seconds()),
        path="/"
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(access_ttl.total_seconds()),
        path="/"
    )
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh(response: Response, request: Request):

    access_ttl = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    refresh_ttl = timedelta(days=settings.REFRESH_TOKEN_EXPIRES)

    current_refresh_token = request.cookies.get("refresh_token")
    if not current_refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    payload = await verify_refresh_token(current_refresh_token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    new_access_token = create_token({"sub": username}, expires_delta=access_ttl, type="access")
    new_refresh_token = create_token({"sub": username}, expires_delta=refresh_ttl, type="refresh")

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(refresh_ttl.total_seconds()),
        path="/"
    )
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(access_ttl.total_seconds()),
        path="/"
    )
    return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)
