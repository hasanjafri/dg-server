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
