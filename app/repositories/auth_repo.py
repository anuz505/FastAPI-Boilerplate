from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from app.models import User
from app.schemas import UserResponse, UserSignUp, UserUpdate
from app.utils.auth_utils import get_password_hash


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self) -> List[UserResponse]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, id: UUID) -> UserResponse:
        result = await self.db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> UserResponse:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, data: UserSignUp) -> UserResponse:
        existing_user = await self.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        user_data = data.model_dump()
        user_data["password"] = get_password_hash(user_data["password"])
        user = User(**user_data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, data: UserUpdate, id: UUID) -> UserResponse:
        user = await self.get_by_id(id)
        if not user:
            raise ValueError("The user does not exist")

        update_data = data.model_dump(exclude_unset=True)
        new_email = update_data.get("email")
        if new_email and new_email != user.email:
            existing_user = await self.get_user_by_email(new_email)
            if existing_user:
                raise ValueError("User with this email already exists")

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user
