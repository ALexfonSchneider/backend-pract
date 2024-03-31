import asyncio
from httpx import ASGITransport, AsyncClient
from src.database import Base
from src.dependencies import get_async_session
from src import config
import pytest
from app import app as app
from sqlalchemy import URL, AsyncAdaptedQueuePool, NullPool, make_url
import tests.db_utils as utils

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

settings = config.Settings()

def test_db_url() -> URL:
    return make_url(f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD.get_secret_value()}@{settings.DB_HOST}:{settings.DB_PORT}/test_{settings.DB_NAME}')

pg_url = test_db_url()

engine = create_async_engine(url=pg_url, poolclass=AsyncAdaptedQueuePool, isolation_level="REPEATABLE READ")
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture()
def client():
    return AsyncClient(transport=ASGITransport(app), base_url="http://test/")
        

async def get_test_async_session():
    async with async_session_maker() as connection:
        return connection


async def initdb():
    await utils.pg_restore_database(pg_url)
    
    engine = create_async_engine(url=pg_url, isolation_level="AUTOCOMMIT")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        
    app.dependency_overrides[get_async_session] = get_test_async_session
    

@pytest.fixture(scope='function')
def session() -> AsyncSession:
    return async_session_maker()
    

def pytest_configure(config):
    asyncio.run(initdb())