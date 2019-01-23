import datetime

from sqlalchemy import (
    Column, Integer, String,
    DateTime, ForeignKey
)

from sqlalchemy.orm import relationship

from app.models import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, autoincrement=True, primary_key=True)

    category_name = Column(String, nullable=False)

    _internal_names = relationship("InternalName", back_populates="category")

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Admin', back_populates="_categories")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        """ Show admin object info. """
        return '<Category: {}>'.format(self.category_name)
    
    def to_dict(self):
        ret = {
            "id": self.id,
            "category_name": self.category_name,
            "project": self.project_id,
            "internal_names": [internal_name.internal_name for internal_name in self._internal_names]
        }
        return ret