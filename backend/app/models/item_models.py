from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

# Association tables for Many-to-Many relationships
item_itempool_association = Table(
    "item_itempool",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
    Column("itempool_id", Integer, ForeignKey("itempools.id"), primary_key=True),
)


class ItemPool(Base):
    __tablename__ = "itempools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    items = relationship(
        "Item", secondary=item_itempool_association, back_populates="item_pools"
    )


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quote = Column(String, nullable=False)
    quality = Column(Integer, nullable=False)

    item_pools = relationship(
        "ItemPool", secondary=item_itempool_association, back_populates="items"
    )


class Trinket(Base):
    __tablename__ = "trinkets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quote = Column(String, nullable=False)
