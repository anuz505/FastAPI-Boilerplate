from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories import TodoRepository
from app.schemas import TodoCreate, TodoResponse, TodoUpdate


class TodoService:
    def __init__(self, db: AsyncSession):
        self.repo = TodoRepository(db)

    async def get_all(self) -> List[TodoResponse]:
        return await self.repo.get_all()

    async def get_or_404(self, id: str) -> TodoResponse:
        todo = await self.repo.get_by_id(id)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo not found {id}")
        return todo

    async def create(self, todo: TodoCreate) -> TodoResponse:
        return await self.repo.create(todo)

    async def update(self, updated_todo: TodoUpdate, id: str) -> TodoResponse:
        todo = await self.get_or_404(id)
        return await self.repo.update(todo, updated_todo)

    async def delete(self, id: str):
        todo = await self.get_or_404(id)
        return await self.repo.delete(todo)
