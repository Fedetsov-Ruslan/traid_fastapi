import time

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


from fastapi_cache.decorator import cache
from src.database import get_async_session
from src.operation.models import operation
from src.operation.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["operations"],
)


@router.get("/long_operation")
@cache(expire=60)
def get_long_op():
    time.sleep(2)
    return "long operation"

@router.get("/")
async def get_specific_operations(operation_type:str, session:AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    operations = result.all()
    return [  {
            "id": op.id,
            "quantity": op.quantity,
            "figi": op.figi,
            "instrument_type": op.instrument_type,
            "date": op.date.isoformat(), 
            "type": op.type
        } for op in operations]


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session:AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': "success"}


