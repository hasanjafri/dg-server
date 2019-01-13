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
    project_id = Column(Integer, ForeignKey('project.id'))
    project = Column("Project", back_populates="users")

    # Methods
    def __repr__(self):
        """ Show user object info. """
        return '<User: {}>'.format(self.id)

    def full_name(self):
        """ Return users full name. """
        return '{} {}'.format(self.first_name, self.last_name)

    def formatted_birthday(self):
        """ Return birthday date in a understandable format. """
        return self.birthday.strftime('%m/%d/%Y')

    def permissions(self):
        """ Return list of this user's permissions """
        return [permission for permission in self._permissions.split(';')]

    def to_dict(self):
        ret = {
            'id': self.id,
            'name': self.full_name(),
            'email': self.email,
            'created_at': format_datetime_object(self.created_at),
            'last_logged_in': format_datetime_object(self.last_logged_in),
            'birthday': self.formatted_birthday(),
            'is_active': self.is_active,
            'api_key': self.api_key,
            'activated_at': self.activated_at,
            'project_id': self.project_id,
            'permissions': self.permissions()
        }
        return ret