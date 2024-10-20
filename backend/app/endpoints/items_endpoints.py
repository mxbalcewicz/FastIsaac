from typing import List

from app.database import get_db
from app.models.item_models import Item
from app.operations.generics import (
    create_multiple_objects_in_db,
    create_object_in_db,
    delete_object_from_db,
)
from app.operations.item_operations import get_item_from_db, get_items_from_db
from app.routers.isaac_routers import isaac_router as router
from app.schemas.item_schemas import ItemCreate, ItemSchema
from fastapi import Depends
from sqlalchemy.orm import Session


@router.get("/item/", response_model=List[ItemSchema])
def get_item_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_items_from_db(db, skip=skip, limit=limit)


@router.get("/item/{item_id}", response_model=ItemSchema)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return get_item_from_db(db, item_id)


@router.post("/item/", response_model=ItemSchema)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_object_in_db(db=db, model_class=Item, obj=item)


@router.post("/item/multiple/", response_model=List[ItemSchema])
def create_item_multiple(items: List[ItemCreate], db: Session = Depends(get_db)):
    return create_multiple_objects_in_db(db, obj_list=items, model_class=Item)


@router.delete("/item/{trinket_id}")
def delete_item(trinket_id: int, db: Session = Depends(get_db)):
    return delete_object_from_db(db, Item, trinket_id)
