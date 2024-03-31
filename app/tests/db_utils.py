import contextlib
from typing import AsyncIterator
import uuid
from alembic.config import Config
import pathlib
import sqlalchemy
import os
from sqlalchemy_utils.functions.database import (
    _set_url_database,
)
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine


def alembic_config(pg_url: URL, alembic_root: str = pathlib.Path().resolve()) -> Config:
    config = Config(os.path.join(alembic_root, "alembic.ini"))
    config.set_main_option('sqlalchemy.url', str(pg_url))
    return config


async def pg_create_database_async(url: URL) -> None:
    database = url.database

    url = _set_url_database(url, database="postgres")
    engine = create_async_engine(url, isolation_level="AUTOCOMMIT")

    async with engine.begin() as conn:
        text = "CREATE DATABASE {}".format(database)
        await conn.execute(sqlalchemy.text(text))

    await engine.dispose()


async def pg_drop_database_async(url: URL) -> None:
    database = url.database

    url = _set_url_database(url, database="postgres")
    engine = create_async_engine(url, isolation_level="AUTOCOMMIT")

    async with engine.begin() as conn:
        version = conn.dialect.server_version_info
        pid_column = "pid" if (version >= (9, 2)) else "procpid"
        text = """
            SELECT pg_terminate_backend(pg_stat_activity.{pid_column})
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{database}'
            AND {pid_column} <> pg_backend_pid();
            """.format(
                pid_column=pid_column, database=database
        )
        await conn.execute(sqlalchemy.text(text))
        
        text = f"DROP DATABASE {database}"
        await conn.execute(sqlalchemy.text(text))
        
    await engine.dispose()


async def pg_restore_database(url: URL):
    url = url.set(database=url.database)
    
    try:
        await pg_drop_database_async(url)
    except:
        pass
    
    await pg_create_database_async(url)