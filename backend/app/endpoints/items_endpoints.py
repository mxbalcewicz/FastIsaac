from app.schemas.item_schemas import ItemSchema, ItemBase
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.operations.item_operations import (
    get_items_from_db,
    create_item,
    get_item_from_db,
)

from fastapi import APIRouter

router = APIRouter()


@router.get("/items/", response_model=List[ItemSchema])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items_from_db(db, skip=skip, limit=limit)
    return items


@router.get("/items/{item_id}", response_model=ItemSchema)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return get_item_from_db(db, item_id)


@router.post("/items/", response_model=ItemBase)
def create_item(item: ItemBase, db: Session = Depends(get_db)):
    return create_item(db=db, item=item)
