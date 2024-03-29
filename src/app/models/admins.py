""" Module represents an Admin. """
import datetime

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Date, Boolean
)

from sqlalchemy.orm import relationship

from app.models import Base
from app.utils.auth import generate_api_key
from app.utils.date_utils import format_datetime_object

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, autoincrement=True, primary_key=True)

    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
    password_salt = Column(String(100), nullable=False)

    api_key = Column(String(45), default=generate_api_key, unique=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_logged_in = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    birthday = Column(Date, nullable=False)
    security_answer = Column(String, nullable=False)
    first_name = Column(String(35), nullable=False)
    last_name = Column(String(35), nullable=False)
    phone_num = Column(String(50), nullable=False)
    country = Column(String(74), nullable=False)
    country_code = Column(String(2), nullable=False)

    is_active = Column(Boolean, default=True)
    activated_at = Column(DateTime, default=datetime.datetime.utcnow)

    subscription_tier = Column(Integer, nullable=False)
    subscription_period = Column(DateTime, nullable=False)

    project = relationship("Project", back_populates="admin")

    def __repr__(self):
        """ Show admin object info. """
        return '<Admin: {}>'.format(self.id)

    def full_name(self):
        """ Return admin's full name. """
        return '{} {}'.format(self.first_name, self.last_name)

    def formatted_birthday(self):
        """ Return birthday date in a understandable format. """
        return self.birthday.strftime('%m/%d/%Y')

    def to_dict(self):
        ret = {
            'id': self.id,
            'name': self.full_name(),
            'email': self.email,
            'password': self.password,
            'password_salt': self.password_salt,
            'tel': self.phone_num,
            'created_at': format_datetime_object(self.created_at),
            'last_logged_in': format_datetime_object(self.last_logged_in),
            'birthday': self.formatted_birthday(),
            'country': self.country + '-' + self.country_code,
            'is_active': self.is_active,
            'api_key': self.api_key,
            'activated_at': self.activated_at,
            'subscription_tier': self.subscription_tier,
            'subscription_period': self.subscription_period,
            'projects': self.project
        }
        return ret

    def project_ids(self):
        return [project.id for project in self.project]