from pydantic import BaseModel

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