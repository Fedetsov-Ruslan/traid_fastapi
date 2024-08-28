from datetime import datetime
from sqlalchemy import TIMESTAMP, MetaData, Integer, String, ForeignKey, Table, Column, JSON, Boolean
from src.database import metadata, Base
from fastapi_users.db import SQLAlchemyBaseUserTable



role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permission", JSON)
)

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column( Integer, primary_key=True)
    email = Column( String, nullable=False)
    username = Column( String, nullable=False)
    role_id = Column( Integer)
    hashed_password = Column( String, nullable=False)
    registered_at = Column( TIMESTAMP, default=datetime.utcnow)
    is_active = Column( Boolean, default=True)
    is_superuser = Column( Boolean,  default=False)
    is_verified = Column( Boolean,  default=False)
