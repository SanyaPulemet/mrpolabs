from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from settings import DATABASE_URL
from typing import AsyncGenerator
from sqla import Base

async_engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind = async_engine,
    expire_on_commit = False,
    class_ = AsyncSession
)

async def create_connection() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session