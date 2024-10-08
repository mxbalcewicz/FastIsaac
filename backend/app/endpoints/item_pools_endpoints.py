from typing import List

from app.database import get_db
from app.models.item_models import ItemPool
from app.operations.generics import (
    create_multiple_objects_in_db,
    create_object_in_db,
    delete_object_from_db,
    get_objects_from_db,
    get_single_object_from_db,
)
from app.routers.isaac_routers import isaac_router as router
from app.schemas.item_schemas import ItemPoolCreate, ItemPoolSchema
from fastapi import Depends
from sqlalchemy.orm import Session


@router.get("/item_pool/", response_model=List[ItemPoolSchema])
def get_item_pool_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_objects_from_db(db, ItemPool, skip, limit)


@router.get("/item_pool/{item_pool_id}", response_model=ItemPoolSchema)
def get_item_pool(item_pool_id: int, db: Session = Depends(get_db)):
    return get_single_object_from_db(db, ItemPool, item_pool_id)


@router.post("/item_pool/", response_model=ItemPoolSchema)
def create_item_pool(item_pool: ItemPoolCreate, db: Session = Depends(get_db)):
    return create_object_in_db(db, ItemPool, item_pool)


@router.post("/item_pool/multiple/", response_model=List[ItemPoolSchema])
def create_item_pool_multiple(
    item_pools: List[ItemPoolCreate], db: Session = Depends(get_db)
):
    return create_multiple_objects_in_db(db, item_pools, ItemPool)


@router.delete("/item_pool/{item_pool_id}")
def delete_item_pool(item_pool_id: int, db: Session = Depends(get_db)):
    return delete_object_from_db(db, ItemPool, item_pool_id)
