from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .association_tables import item_pool_association
from ..database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    quote = Column(String)
    quality = Column(Integer, default=0)
    pools = relationship("ItemPool", secondary=item_pool_association, back_populates="items")


class Trinket(Base):
    __tablename__ = "trinkets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    quote = Column(String)


class ItemPool(Base):
    __tablename__ = "item_pools"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    items = relationship("Item", secondary=item_pool_association, back_populates="pools")