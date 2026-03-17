from typing import List
from fastapi import Depends, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user_schema import UserResponse, UserSignUp, UserUpdate
from app.core import LoggerSetup
from app.services import AuthService

logger = LoggerSetup.setup_logger(__name__)
auth_router = APIRouter(prefix="/auth", tags=["auth"])


def get_service(db: Session = Depends(get_db)) -> AuthService:
    logger.info("starting auth service")
    return AuthService(db)


@auth_router.get("/", response_model=List[UserResponse])
async def get_all_users(service: AuthService = Depends(get_service)):
    logger.info("getting all users")
    return await service.get_all_users()


@auth_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserSignUp, service: AuthService = Depends(get_service)):
    logger.info("creating user")
    return await service.create_user(data)


@auth_router.put("/{id}", response_model=UserResponse)
async def update_user(data: UserUpdate, id, service: AuthService = Depends(get_service)):
    logger.info("Update user")
    return await service.update_user(data, id)
