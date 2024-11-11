from typing import List

from app.auth.auth_bearer import JWTBearer
from app.database import get_db
from app.models.item_models import Item
from app.models.user_models import User
from app.operations.generics import (create_multiple_objects_in_db,
                                     create_object_in_db,
                                     delete_object_from_db)
from app.operations.item_operations import get_item_from_db, get_items_from_db
from app.operations.user_operations import get_current_user
from app.schemas.item_schemas import ItemCreate, ItemSchema
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/item/", response_model=List[ItemSchema])
def get_item_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_items_from_db(db, skip=skip, limit=limit)


@router.get("/item/{item_id}", response_model=ItemSchema)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return get_item_from_db(db, item_id)


@router.post("/item/", response_model=ItemSchema)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_object_in_db(db=db, model_class=Item, obj=item)


@router.post("/item/multiple/", response_model=List[ItemSchema])
def create_item_multiple(items: List[ItemCreate], db: Session = Depends(get_db)):
    return create_multiple_objects_in_db(db, obj_list=items, model_class=Item)


@router.delete("/item/{trinket_id}")
def delete_item(trinket_id: int, db: Session = Depends(get_db)):
    return delete_object_from_db(db, Item, trinket_id)


@router.get(
    "/item/favorites",
    response_model=List[ItemSchema],
    dependencies=[Depends(JWTBearer())],
)
def get_user_favorites(user: User = Depends(get_current_user)):
    return user.favorite_items


@router.post("/item/favorites/{item_id}", response_model=ItemSchema)
def add_favorite_item(
    item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")

    if item in user.favorite_items:
        raise HTTPException(status_code=400, detail="Item already in favorites.")

    user.favorite_items.append(item)
    db.commit()
    db.refresh(user)

    return item


@router.delete("/item/favorites/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite_item(
    item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    """Remove an item from the user's favorites."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")

    if item not in user.favorite_items:
        raise HTTPException(status_code=400, detail="Item is not in favorites.")

    user.favorite_items.remove(item)
    db.commit()

    return {"detail": "Item removed from favorites."}
