from sqlalchemy.orm import Session
from .models.item import Item, Trinket, ItemPool
from .schemas import item as item_schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: Item):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_trinkets(db: Session, skip: int=0, limit: int = 100):
    return db.query(Trinket).offset(skip).limit(limit).all()


def create_trinket(db: Session, trinket: item_schemas.TrinketSchema):
    db_trinket = Trinket(**trinket.model_dump())
    db.add(db_trinket)
    db.commit()
    db.refresh(db_trinket)
    return db_trinket


def create_item_pool(db: Session, item_pool: ItemPool):
    db_item_pool = ItemPool(**item_pool.model_dump())
    db.add(db_item_pool)
    db.commit()
    db.refresh(db_item_pool)
    return db_item_pool

def get_item_pools(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ItemPool).offset(skip).limit(limit).all()

def create_item_pool(db: Session, item_pool: ItemPool):
    db_item_pool = ItemPool(**item_pool.model_dump())
    db.add(db_item_pool)
    db.commit()
    db.refresh(db_item_pool)
    return db_item_pool