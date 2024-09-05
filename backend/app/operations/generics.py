from sqlalchemy.orm import Session

from sqlalchemy.orm import Session
from app.models.item_models import Item


def get_objects_from_db(db: Session, model_class, skip: int, limit: int):
    return db.query(model_class).offset(skip).limit(limit).all()


def get_single_object_from_db(db: Session, model_class, id: int):
    return db.query(model_class).filter(model_class.id == id).one()


def create_object_in_db(db: Session, model_class, obj):
    db_obj = model_class(**obj.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
