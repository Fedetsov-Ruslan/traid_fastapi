from datetime import datetime
from sqlalchemy import TIMESTAMP, MetaData, Integer, String, ForeignKey, Table, Column, JSON, Boolean
from src.database import metadata



role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permission", JSON)
)

users = Table(
    "user",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('username', String, nullable=False),
    Column('role_id', Integer, ForeignKey("role.id")),
    Column('hashed_password', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
    Column('is_active', Boolean, default=True),
    Column('is_superuser', Boolean,  default=False),
    Column('is_verified', Boolean,  default=False),
)

