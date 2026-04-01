import pytest
from sqlalchemy import NullPool
from app.models.db_models import Base
from .todo.factories import TodoFactory
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from app.core.config import settings
from dotenv import load_dotenv
import os

load_dotenv()
engine_kwargs = {
    "url": os.getenv("TEST_DB_URL"),
    "echo": settings.debug,
    "future": True,
    "pool_pre_ping": True,
}

if settings.debug:
    engine_kwargs["poolclass"] = NullPool

engine: AsyncEngine = create_async_engine(**engine_kwargs)
TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db():
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
            await session.rollback()


@pytest.fixture
async def todo(db):
    TodoFactory._meta.sqlalchemy_session = db
    try:
        todo = TodoFactory()
        await db.flush()
        await db.refresh(todo)
        return todo
    finally:
        TodoFactory._meta.sqlalchemy_session = None
