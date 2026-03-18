from typing import List
from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies import get_current_user
from app.schemas.todo_schema import TodoCreate, TodoResponse, TodoUpdate, UserTodoResponses
from app.services import TodoService
from uuid import UUID
from app.core import LoggerSetup
from app.services.auth_service import AuthService

logger = LoggerSetup.setup_logger(__name__)
todo_router = APIRouter(prefix="/todo", tags=["todos"], dependencies=[Depends(get_current_user)])


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    logger.info("starting service")
    return TodoService(db)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    logger.info("starting service")
    return AuthService(db)


@todo_router.get("/", response_model=List[TodoResponse])
async def get_all_todos(service: TodoService = Depends(get_todo_service)):
    logger.info("gettings all todos")
    return await service.get_all()


@todo_router.get("/users", response_model=UserTodoResponses)
async def users_todo(
    auth_service: AuthService = Depends(get_auth_service),
    current_user: dict = Depends(get_current_user),
    todo_service: TodoService = Depends(get_todo_service),
):
    logger.info("getting all users todo")
    username = current_user.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = await auth_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    todos = await todo_service.get_users_all(user_id=user.id)
    return UserTodoResponses(user_id=user.id, todos=todos)


@todo_router.get("/{id}")
async def get_todo_detail(id: UUID, service: TodoService = Depends(get_todo_service)):
    logger.info(f"getting todo {id}")
    return await service.get_or_404(id)


@todo_router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    data: TodoCreate,
    auth_service: AuthService = Depends(get_auth_service),
    current_user: dict = Depends(get_current_user),
    service: TodoService = Depends(get_todo_service),
):
    logger.info("creating todo")
    username = current_user.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = await auth_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await service.create(data, owner_id=user.id)


@todo_router.put("/{id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def update_todo(id: UUID, data: TodoUpdate, service: TodoService = Depends(get_todo_service)):
    logger.info("updating todo")
    return await service.update(data, id)


@todo_router.delete("/{id}")
async def delete_todo(id: UUID, service: TodoService = Depends(get_todo_service)):
    logger.info("deleting todo")
    return await service.delete(id)
