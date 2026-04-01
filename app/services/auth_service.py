from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories import AuthRepository
from app.schemas import UserResponse, UserSignUp, UserUpdate
from uuid import UUID


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = AuthRepository(db)

    async def get_all_users(self) -> List[UserResponse]:
        return await self.repo.get_all_users()

    async def create_user(self, data: UserSignUp) -> UserResponse:
        try:
            return await self.repo.create_user(data)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    async def update_user(self, data: UserUpdate, id: UUID) -> UserResponse:
        try:
            return await self.repo.update_user(data, id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    async def get_user_by_username(self, username: str) -> UserResponse:
        try:
            return await self.repo.get_user_by_username(username)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
