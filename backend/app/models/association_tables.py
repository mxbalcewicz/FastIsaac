
from sqlalchemy import Table, Column, Integer, ForeignKey
from ..database import Base

item_pool_association = Table(
    'item_pool_m2m', Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id'), primary_key=True),
    Column('item_pool_id', Integer, ForeignKey('item_pools.id'), primary_key=True)
)