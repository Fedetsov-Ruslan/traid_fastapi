from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI
from fastapi_users import  FastAPIUsers, fastapi_users
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, Field
from enum import Enum
from src.auth.auth import auth_backend
from src.database import User, get_user_db
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead
from src.operation.router import router as operation_router
from src.tasks.router import router as tasks_router
from src.pages.router import router as pages_router
from src.chat.router import router as chat_router


async def lifespan(app: FastAPI):
    # Код для инициализации при старте приложения
    redis = aioredis.from_url('redis://localhost', decode_responses=True, encoding='utf-8')
    FastAPICache.init(RedisBackend(redis=redis), prefix="fastapi-cache")

    yield
    await redis.close()

app = FastAPI(lifespan=lifespan, title='Trading app')
app.mount('/static', StaticFiles(directory='src/static'), name='static')

class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType

class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str
    price: float = Field(ge=0)
    quantity: float

class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[list[Degree]] =[]


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(operation_router)
app.include_router(tasks_router)
app.include_router(pages_router)
app.include_router(chat_router)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



