from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    quote = Column(String)
    description = Column(String)
    quality = Column(Integer, index=True)

class ItemPool(Base):
    __tablename__ = "item_pools"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    items = relationship("Item", secondary="pool_item", back_populates='pools') # Review relationships
    