from fastapi.routing import APIRouter

from ..schemas import user as user_schemas
from ..schemas import item as item_schemas
from ..models import item as item_models
from .. import crud
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.get("/items/", response_model=List[item_schemas.ItemBase])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.post("/items/", response_model=item_schemas.ItemBase)
def create_item(item: item_schemas.ItemBase, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@router.get("/trinkets/", response_model=List[item_schemas.TrinketBase])
def read_trinkets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_trinkets(db, skip=skip, limit=limit)
    return items


@router.post("/trinkets/", response_model=item_schemas.TrinketBase)
def create_trinket(item: item_schemas.TrinketBase, db: Session = Depends(get_db)):
    return crud.creat(db=db, item=item)