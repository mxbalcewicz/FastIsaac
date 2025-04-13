from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.item_models import Trinket
from app.operations.generics import (
    create_multiple_objects_in_db,
    create_object_in_db,
    delete_object_from_db,
    get_objects_from_db,
    get_single_object_from_db,
)
from app.schemas.item_schemas import TrinketCreate, TrinketSchema

router = APIRouter()


@router.get("/trinket/", response_model=List[TrinketSchema])
async def get_trinket_all(limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_objects_from_db(db, Trinket, limit)


@router.get("/trinket/{trinket_id}", response_model=TrinketSchema)
async def get_trinket(trinket_id: int, db: AsyncSession = Depends(get_db)):
    return await get_single_object_from_db(db, Trinket, trinket_id)


@router.post("/trinket/", response_model=TrinketSchema)
async def create_trinket(trinket: TrinketCreate, db: AsyncSession = Depends(get_db)):
    return await create_object_in_db(db, Trinket, trinket)


@router.post("/trinket/multiple/", response_model=List[TrinketSchema])
async def create_trinket_multiple(trinkets: List[TrinketCreate], db: AsyncSession = Depends(get_db)):
    return await create_multiple_objects_in_db(db, trinkets, Trinket)


@router.delete("/trinket/{trinket_id}")
async def delete_trinket(trinket_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_object_from_db(db, Trinket, trinket_id)
