from typing import List, Optional
from pydantic import BaseModel


class ItemPool(BaseModel):
    id: int
    name: str


class Item(BaseModel):
    id: int
    name: str
    description: str
    quote: str
    quality: int
    item_pools: List[ItemPool]


class Trinket(BaseModel):
    id: int
    name: str
    description: str
    quote: str
    item_pools: List[ItemPool]