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

    project_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)

    admin_id = Column(Integer, ForeignKey('admins.id'))
    admin = relationship('Admin', back_populates="project")

    users = relationship('User', back_populates="project")
    _suppliers = relationship('Supplier', back_populates="project")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        """ Show project object info. """
        return '<Project: {}>'.format(self.project_name)

    def suppliers(self):
        return self._suppliers.split(';')

    def to_dict(self):
        ret = {
            'id': self.id,
            'project_name': self.project_name,
            'address': self.address,
            'postal_code': self.postal_code,
            'last_updated': self.last_updated,
            'num_users': len(self.users)
        }
        return ret

    def users_list(self):
        return [user.to_dict() for user in self.users]