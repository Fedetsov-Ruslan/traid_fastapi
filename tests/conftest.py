import asyncio
import os
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

from src.database import get_async_session
from src.database import metadata


from src.main import app

env_vars_to_clear = ['DB_NAME', 'DB_USER', 'DB_PASS', 'DB_HOST',  'MODE']

for var in env_vars_to_clear:
    os.environ.pop(var, None)
load_dotenv('.test.env')
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
MODE = os.environ.get("MODE")

#DataBase
DATABASE_URL_TEST = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
print(DATABASE_URL_TEST, MODE)
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session



@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    assert MODE == 'TEST'
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


#SETUP
@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client = TestClient(app)



@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac