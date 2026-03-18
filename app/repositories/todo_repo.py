from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Todo
from app.schemas.todo_schema import TodoCreate, TodoResponse, TodoUpdate


class TodoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[TodoResponse]:
        result = await self.db.execute(select(Todo))
        return result.scalars().all()

    async def get_users_all(self, user_id: UUID) -> List[TodoResponse]:
        result = await self.db.execute(select(Todo).where(Todo.owner_id == user_id))
        return result.scalars().all()

    async def get_by_id(self, id: UUID):
        result = await self.db.execute(select(Todo).where(Todo.id == id))
        return result.scalar_one_or_none()

    async def create(self, data: TodoCreate, owner_id: UUID) -> TodoResponse:
        todo = Todo(**data.model_dump(), owner_id=owner_id)
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        return todo

    async def update(self, todo: Todo, data: TodoUpdate) -> TodoResponse:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)
        await self.db.commit()
        await self.db.refresh(todo)
        return todo

    async def delete(self, todo: Todo):
        await self.db.delete(todo)
        await self.db.commit()
