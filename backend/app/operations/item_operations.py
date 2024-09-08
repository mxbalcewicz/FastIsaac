from app.models.item_models import Item
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload


def get_items_from_db(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Item)
        .options(joinedload(Item.item_pools))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_item_from_db(db: Session, item_id: int):
    item = (
        db.query(Item)
        .options(joinedload(Item.item_pools))
        .filter(Item.id == item_id)
        .one_or_none()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
