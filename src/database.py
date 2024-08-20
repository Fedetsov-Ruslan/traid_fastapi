import datetime
import os
from typing import AsyncGenerator, Optional

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Integer, MetaData
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS


DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
Base: DeclarativeMeta = declarative_base()

metadata = MetaData()

class User(SQLAlchemyBaseUserTableUUID, Base):
    id = Column( Integer, primary_key=True)
    email = Column( String, nullable=False)
    username = Column( String, nullable=False)
    role_id = Column( Integer)
    
    


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


