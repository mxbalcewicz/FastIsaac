from sqlalchemy.orm import Session
from .models import item as item_models
from .schemas import item as item_schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(item_models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: item_schemas.ItemCreate):
    db_item = item_models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_trinkets(db: Session, skip: int=0, limit: int = 100):
    return db.query(item_models.Trinket).offset(skip).limit(limit).all()


def create_trinket(db: Session, trinket: item_schemas.TrinketCreate):
    db_trinket = item_models.Trinket(**trinket.model_dump())
    db.add(db_trinket)
    db.commit()
    db.refresh(db_trinket)
    return db_trinket