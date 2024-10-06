from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict


class ItemPoolBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    wiki_id: str
    name: str
    description: str
    quote: str
    quality: int

    model_config = ConfigDict(from_attributes=True)


class TrinketBase(BaseModel):
    wiki_id: str
    name: str
    description: str
    quote: str

    model_config = ConfigDict(from_attributes=True)


class ItemPoolCreate(ItemPoolBase):
    pass


class TrinketCreate(TrinketBase):
    pass


class ItemCreate(ItemBase):
    pass


class ItemPoolSchema(ItemPoolBase):
    id: int
    items: List["ItemSchema"]


class ItemSchema(ItemBase):
    id: int
    item_pools: Union[List[ItemPoolBase], None] = []


class TrinketSchema(TrinketBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
