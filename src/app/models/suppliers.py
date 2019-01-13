import datetime

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Date, Boolean
)

from sqlalchemy.orm import relationship

from app.models import Base

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, autoincrement=True, primary_key=True)
    
    name = Column(String, nullable=False, unique=True)
    food_items = relationship("InventoryProduct", back_populates="supplier")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)