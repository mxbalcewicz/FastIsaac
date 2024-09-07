from typing import List

from app.models.item_models import Item
from fastapi import Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session


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


def create_multiple_objects_in_db(
    db: Session, objects_list: List[BaseModel], model_class
):
    db_objects = []
    for obj in objects_list:
        db_object = model_class(**obj.model_dump())
        db_objects.append(db_object)
    db.bulk_save_objects(db_objects)
    db.commit()
    return db_objects


def delete_object_from_db(db: Session, model_class, id: int):
    db_obj = get_single_object_from_db(db, model_class, id)
    db.delete(db_obj)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Object with id {id} deleted successfully"},
    )
