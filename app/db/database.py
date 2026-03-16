from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from app.core import settings
from app.models import Base

engine_kwargs = {
    "url": settings.db_url,
    "echo": settings.debug,
    "future": True,
    "pool_pre_ping": True,
}

if settings.debug:
    engine_kwargs["poolclass"] = NullPool

engine: AsyncEngine = create_async_engine(**engine_kwargs)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
