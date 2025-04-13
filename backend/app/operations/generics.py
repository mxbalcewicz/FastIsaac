from typing import List

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_objects_from_db(db: AsyncSession, model_class, limit: int):
    result = await db.execute(select(model_class).limit(limit))
    return result.scalars().all()


async def get_single_object_from_db(db: AsyncSession, model_class, id: int):
    result = await db.execute(select(model_class).where(model_class.id == id))
    db_object = result.scalar_one_or_none()
    if not db_object:
        raise HTTPException(status_code=404, detail="Not found")
    return db_object


async def create_object_in_db(db: AsyncSession, model_class, obj):
    db_obj = model_class(**obj.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def create_multiple_objects_in_db(db: AsyncSession, objects_list: List[BaseModel], model_class):
    db_objects = [model_class(**obj.model_dump()) for obj in objects_list]
    db.add_all(db_objects)
    await db.commit()
    return db_objects


async def delete_object_from_db(db: AsyncSession, model_class, id: int):
    db_obj = await get_single_object_from_db(db, model_class, id)
    await db.delete(db_obj)
    await db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Object with id {id} deleted successfully"},
    )
