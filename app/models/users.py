""" Module represents a User. """

import datetime

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Date, Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.models import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)

    # Authentication Attributes.
    email = Column(String(255), nullable=False)
    password = Column(String(500), nullable=True)
    password_salt = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_logged_in = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Personal Attributes.
    birthday = Column(Date, nullable=True)
    first_name = Column(String(35), nullable=True)
    last_name = Column(String(35), nullable=True)
    phone_num = Column(String(50), nullable=True)

    # Permission Based Attributes.
    is_active = Column(Boolean, default=False)
    activated_at = Column(DateTime, nullable=True, default=None)

    # Relationships
    project_id = Column(Integer, ForeignKey('projects.id'))

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