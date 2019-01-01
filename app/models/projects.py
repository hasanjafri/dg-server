""" Module represents a Project. """
import datetime

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Date, Boolean,
    ForeignKey, PickleType
)

from sqlalchemy.orm import relationship

from app.models import Base

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, autoincrement=True, primary_key=True)

    categories = Column(PickleType, nullable=True)

    admin_id = Column(Integer, ForeignKey('admins.id'))
    admin = relationship('Admin', back_populates="project")

    users = relationship('User')

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)