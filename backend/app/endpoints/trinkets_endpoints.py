from typing import List

from app.database import get_db
from app.models.item_models import Trinket
from app.operations.generics import (
    create_multiple_objects_in_db,
    create_object_in_db,
    delete_object_from_db,
    get_objects_from_db,
    get_single_object_from_db,
)
from app.routers.isaac_routers import isaac_router as router
from app.schemas.item_schemas import TrinketCreate, TrinketSchema
from fastapi import Depends
from sqlalchemy.orm import Session


@router.get("/trinket/", response_model=List[TrinketSchema])
def get_trinket_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_objects_from_db(db, Trinket, skip, limit)


@router.get("/trinket/{trinket_id}", response_model=TrinketSchema)
def get_trinket(trinket_id: int, db: Session = Depends(get_db)):
    return get_single_object_from_db(db, Trinket, trinket_id)


@router.post("/trinket/", response_model=TrinketSchema)
def create_trinket(trinket: TrinketCreate, db: Session = Depends(get_db)):
    return create_object_in_db(db, Trinket, trinket)


@router.post("/trinket/multiple/", response_model=List[TrinketSchema])
def create_trinket_multiple(
    trinkets: List[TrinketCreate], db: Session = Depends(get_db)
):
    return create_multiple_objects_in_db(db, trinkets, Trinket)


@router.delete("/trinket/{trinket_id}")
def delete_trinket(trinket_id: int, db: Session = Depends(get_db)):
    return delete_object_from_db(db, Trinket, trinket_id)
