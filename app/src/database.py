from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.orm import DeclarativeBase
from src.config import Settings

settings = Settings()

print(settings.DATABASE_URL_asyncpg)

engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, poolclass=AsyncAdaptedQueuePool, isolation_level="REPEATABLE READ")
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass