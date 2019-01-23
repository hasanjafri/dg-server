import datetime

from sqlalchemy import (
    Column, Integer, String,
    DateTime, ForeignKey
)

from sqlalchemy.orm import relationship

from app.models import Base
from app.utils.date_utils import format_datetime_object

class InternalName(Base):
    __tablename__ = 'internal_names'

    id = Column(Integer, autoincrement=True, primary_key=True)

    internal_name = Column(String, nullable=False)

    _food_items = relationship('InventoryProduct', back_populates='internal_name')

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates="_internal_names")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    def __repr__(self):
        """ Show admin object info. """
        return '<Internal Name: {}>'.format(self.internal_name)

    def to_dict(self):
        ret = {
            'id': self.id,
            'internal_name': self.internal_name,
            'category_id': self.category_id,
            'last_updated': format_datetime_object(self.last_updated),
        }
        return ret