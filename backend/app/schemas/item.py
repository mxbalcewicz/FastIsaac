from pydantic import BaseModel

from typing import List, Optional


class ItemBase(BaseModel):
    id: int
    name: str
    description: str
    quote : str
    quality: int | None = 0

    class Config:
        from_attributes = True


class TrinketBase(BaseModel):
    id: int
    name: str
    description: str
    quote : str

    class Config:
        from_attributes = True

class ItemPoolBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ItemSchema(ItemBase):
    pools: List[ItemBase]


class ItemPoolSchema(ItemPoolBase):
    items: List[ItemBase]