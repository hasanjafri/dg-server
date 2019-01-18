""" Module represents a User. """

import datetime

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.models import Base
from app.utils.auth import generate_api_key
from app.utils.date_utils import format_datetime_object

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)

    # Authentication Attributes.
    user_name = Column(String(255), unique=True, nullable=False)
    password = Column(String(500), nullable=False)
    password_salt = Column(String(100), nullable=False)

    api_key = Column(String(45), default=generate_api_key, unique=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_logged_in = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Permission Based Attributes.
    is_active = Column(Boolean, default=True)
    activated_at = Column(DateTime, default=datetime.datetime.utcnow)
    _permissions = Column(String, default='')

    # Relationships
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="users")

    # Methods
    def __repr__(self):
        """ Show user object info. """
        return '<User: {}>'.format(self.id)

    def formatted_birthday(self):
        """ Return birthday date in a understandable format. """
        return self.birthday.strftime('%m/%d/%Y')

    def permissions(self):
        """ Return list of this user's permissions """
        return self._permissions.split(';')

    def to_dict(self):
        ret = {
            'id': self.id,
            'email': self.email,
            'created_at': format_datetime_object(self.created_at),
            'last_logged_in': format_datetime_object(self.last_logged_in),
            'is_active': self.is_active,
            'api_key': self.api_key,
            'activated_at': self.activated_at,
            'project': self.project.to_dict(),
            'permissions': self.permissions()
        }
        return ret