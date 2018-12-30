""" Module represents an Admin. """
import datetime

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Date, Boolean
)

from sqlalchemy.orm import relationship

from app.models import Base
from app.utils.auth import generate_api_key

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, autoincrement=True, primary_key=True)

    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(500), nullable=True)
    password_salt = Column(String(100), nullable=True)

    api_key = Column(String(45), default=generate_api_key, unique=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_logged_in = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    birthday = Column(Date, nullable=False)
    first_name = Column(String(35), nullable=False)
    last_name = Column(String(35), nullable=False)
    phone_num = Column(String(50), nullable=True)

    is_active = Column(Boolean, default=False)
    activated_at = Column(DateTime, nullable=True, default=None)

    subscription_tier = Column(Integer, nullable=False)

    project = relationship("Project", uselist=False, back_populates="admin", nullable=True)

    def __repr__(self):
        """ Show admin object info. """
        return '<Admin: {}>'.format(self.id)

    def full_name(self):
        """ Return admin's full name. """
        return '{} {}'.format(self.first_name, self.last_name)

    def formatted_birthday(self):
        """ Return birthday date in a understandable format. """
        return self.birthday.strftime('%m/%d/%Y')