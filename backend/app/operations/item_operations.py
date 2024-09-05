from sqlalchemy.orm import Session
from app.models.item_models import Item
from sqlalchemy.orm import Session, joinedload


def get_items_from_db(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Item)
        .options(joinedload(Item.item_pools))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_item(db: Session, item: Item):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item_from_db(db: Session, item_id: int):
    return (
        db.query(Item)
        .options(joinedload(Item.item_pools))
        .filter(Item.id == item_id)
        .one()
    )
