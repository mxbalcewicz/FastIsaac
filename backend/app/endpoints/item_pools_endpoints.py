from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.item_models import ItemPool
from app.operations.generics import (
    create_multiple_objects_in_db,
    create_object_in_db,
    delete_object_from_db,
    get_objects_from_db,
    get_single_object_from_db,
)
from app.schemas.item_schemas import ItemPoolCreate, ItemPoolSchema

router = APIRouter()


@router.get("/item_pool/", response_model=List[ItemPoolSchema])
async def get_item_pool_all(limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_objects_from_db(db, ItemPool, limit)


@router.get("/item_pool/{item_pool_id}", response_model=ItemPoolSchema)
async def get_item_pool(item_pool_id: int, db: AsyncSession = Depends(get_db)):
    return await get_single_object_from_db(db, ItemPool, item_pool_id)


@router.post("/item_pool/", response_model=ItemPoolSchema)
async def create_item_pool(item_pool: ItemPoolCreate, db: AsyncSession = Depends(get_db)):
    return await create_object_in_db(db, ItemPool, item_pool)


@router.post("/item_pool/multiple/", response_model=List[ItemPoolSchema])
async def create_item_pool_multiple(item_pools: List[ItemPoolCreate], db: AsyncSession = Depends(get_db)):
    return await create_multiple_objects_in_db(db, item_pools, ItemPool)


@router.delete("/item_pool/{item_pool_id}")
async def delete_item_pool(item_pool_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_object_from_db(db, ItemPool, item_pool_id)
