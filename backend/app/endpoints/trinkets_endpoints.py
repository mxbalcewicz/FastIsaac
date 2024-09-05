from app.schemas.item_schemas import TrinketSchema
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.item_models import Trinket
from app.operations.generics import get_objects_from_db, create_object_in_db

from fastapi import APIRouter

router = APIRouter()


@router.get("/trinkets/", response_model=List[TrinketSchema])
def read_trinkets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_objects_from_db(db, Trinket, skip, limit)


@router.post("/trinkets/", response_model=TrinketSchema)
def create_trinket(trinket: TrinketSchema, db: Session = Depends(get_db)):
    return create_object_in_db(db, Trinket, trinket)
