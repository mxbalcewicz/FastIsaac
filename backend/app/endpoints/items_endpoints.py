from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.auth_bearer import JWTBearer
from app.database import get_db
from app.models.item_models import Item
from app.models.user_models import User
from app.operations.generics import (
    create_multiple_objects_in_db,
    create_object_in_db,
    delete_object_from_db,
)
from app.operations.item_operations import get_item_from_db, get_items_from_db
from app.operations.user_operations import get_current_user
from app.schemas.item_schemas import ItemCreate, ItemSchema

router = APIRouter()


@router.get("/item/", response_model=List[ItemSchema])
async def get_item_all(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_items_from_db(db, skip=skip, limit=limit)


@router.get("/item/{item_id}", response_model=ItemSchema)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await get_item_from_db(db, item_id)


@router.post("/item/", response_model=ItemSchema)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_object_in_db(db=db, model_class=Item, obj=item)


@router.post("/item/multiple/", response_model=List[ItemSchema])
async def create_item_multiple(items: List[ItemCreate], db: AsyncSession = Depends(get_db)):
    return await create_multiple_objects_in_db(db, obj_list=items, model_class=Item)


@router.delete("/item/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_object_from_db(db, Item, item_id)


@router.get(
    "/item/favorites",
    response_model=List[ItemSchema],
    dependencies=[Depends(JWTBearer())],
)
async def get_user_favorites(user: User = Depends(get_current_user)):
    return user.favorite_items


@router.post("/item/favorites/{item_id}", response_model=ItemSchema)
async def add_favorite_item(item_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")

    if item in user.favorite_items:
        raise HTTPException(status_code=400, detail="Item already in favorites.")

    user.favorite_items.append(item)
    await db.commit()
    await db.refresh(user)

    return item


@router.delete("/item/favorites/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite_item(
    item_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")

    if item not in user.favorite_items:
        raise HTTPException(status_code=400, detail="Item is not in favorites.")

    user.favorite_items.remove(item)
    await db.commit()

    return {"detail": "Item removed from favorites."}
