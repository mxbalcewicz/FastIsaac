from pydantic import BaseModel

from typing import List

class ItemBase(BaseModel):
    name: str
    description: str
    quote : str
    quality: int | None = 0


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class TrinketBase(BaseModel):
    name: str
    description: str
    quote : str

class TrinketCreate(TrinketBase):
    pass

class Trinket(TrinketBase):
    id: int

    class Config:
        orm_mode = True


class ItemPool(BaseModel):
    name: str
    items: List[ItemBase]