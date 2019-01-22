import datetime

from sqlalchemy import (
    Column, Integer, String,
    DateTime
)

from sqlalchemy.orm import relationship

from app.models import Base

class InternalName(Base):
    __tablename__ = 'internal_names'

    id = Column(Integer, autoincrement=True, primary_key=True)

    internal_name = Column(String, nullable=False)

    _food_items = relationship('InventoryProduct', back_populates='internal_name')

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    