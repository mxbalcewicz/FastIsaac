from typing import List, Optional, Union
from pydantic import BaseModel, ConfigDict

class ItemPoolBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    id: int
    name: str
    description: str
    quote: str
    quality: int

    model_config = ConfigDict(from_attributes=True)


class TrinketBase(BaseModel):
    id: int
    name: str
    description: str
    quote: str

    model_config = ConfigDict(from_attributes=True)



class ItemPoolSchema(ItemPoolBase):
    items: List[ItemBase]


class ItemSchema(ItemBase):
    item_pools: Union[List[ItemPoolBase], None] = []


class TrinketSchema(TrinketBase):
    pass