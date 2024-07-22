from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from ..database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    quote = Column(String)
    quality = Column(Integer, default=0)
