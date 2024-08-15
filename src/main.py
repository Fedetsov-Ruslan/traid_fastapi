from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI
from fastapi_users import  FastAPIUsers, fastapi_users
from pydantic import BaseModel, Field
from enum import Enum
from src.auth.auth import auth_backend
from src.database import User, get_user_db
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead
from src.operation.router import router as operation_router

app = FastAPI(
    title='Trading app'
)


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

