from app.schemas.item_schemas import ItemPoolSchema, ItemPoolSchema, ItemPoolBase
from app.routers.isaac_routers import isaac_router as router
from typing import List
from app.models.item_models import ItemPool

from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.operations.generics import create_object_in_db, get_objects_from_db


from fastapi import APIRouter

router = APIRouter()


@router.get("/item_pools/", response_model=List[ItemPoolSchema])
def read_item_pool(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_objects_from_db(db, ItemPool, skip, limit)


@router.post("/item_pool/", response_model=ItemPoolBase)
def create_item_pool(item_pool: ItemPoolBase, db: Session = Depends(get_db)):
    return create_object_in_db(db, ItemPool, item_pool)
