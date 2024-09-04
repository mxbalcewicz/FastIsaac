from fastapi.routing import APIRouter

from ..schemas.item import ItemSchema, TrinketSchema, ItemPoolSchema, ItemPoolSchema, ItemPoolBase, ItemBase
from .. import crud
from typing import List
from ..models.item import Item

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db

router = APIRouter()


@router.get("/items/", response_model=List[ItemSchema])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@router.get("/items/{item_id}", response_model=ItemSchema)
def get_item(item_id : int, db: Session = Depends(get_db)):
    item = db.query(Item).options(joinedload(Item.item_pools)).filter(Item.id == item_id).one()
    item_dict = {
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "quote": item.quote,
        "quality": item.quality,
        "pools": [
            {"id": pool.id, "name": pool.name}
            for pool in item.item_pools  # Mapping each related pool to ItemPoolBase format
        ],
    }
    return item_dict


@router.post("/items/", response_model=ItemBase)
def create_item(item: ItemBase, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@router.get("/trinkets/", response_model=List[TrinketSchema])
def read_trinkets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_trinkets(db, skip=skip, limit=limit)
    return items


@router.post("/trinkets/", response_model=TrinketSchema)
def create_trinket(trinket: TrinketSchema, db: Session = Depends(get_db)):
    return crud.create_trinket(db=db, trinket=trinket)


@router.get("/item_pools/", response_model=List[ItemPoolSchema])
def read_item_pool(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_item_pools(db, skip=skip, limit=limit)
    return items


@router.post("/item_pool/", response_model=ItemPoolBase)
def create_item_pool(item_pool: ItemPoolBase, db: Session = Depends(get_db)):
    return crud.create_item_pool(db=db, item_pool=item_pool)