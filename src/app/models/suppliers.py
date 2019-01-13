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

    def __repr__(self):
        """ Show supplier object info. """
        return '<Supplier: {}>'.format(self.name)

    def to_dict(self):
        ret = {
            'id': self.id,
            'name': self.name,
            'food_items': [food_item.to_dict() for food_item in self.food_items]
        }
        return ret
