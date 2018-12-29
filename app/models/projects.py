""" Module represents a Project. """

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Date, Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.models import Base

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, autoincrement=True, primary_key=True)

    admin_id = Column(Integer, ForeignKey('admin.id'))
    admin = relationship('Admin', back_populates="project")

    users = relationship('User')