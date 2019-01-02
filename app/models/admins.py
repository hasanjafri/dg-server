""" Module represents an Admin. """
from sqlalchemy import (
    Column, String, Integer,
    DateTime, Date, Boolean,
    func
)

from sqlalchemy.orm import relationship

from app.models import Base
from app.utils.auth import generate_api_key

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, autoincrement=True, primary_key=True)

    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
    password_salt = Column(String(100), nullable=False)

    api_key = Column(String(45), default=generate_api_key, unique=True)

    created_at = Column(DateTime, server_default=func.now())
    last_logged_in = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    birthday = Column(Date, nullable=False)
    first_name = Column(String(35), nullable=False)
    last_name = Column(String(35), nullable=False)
    phone_num = Column(String(50), nullable=False)
    country = Column(String(74), nullable=False)
    country_code = Column(String(2), nullable=False)

    is_active = Column(Boolean, default=False)
    activated_at = Column(DateTime, server_default=func.now())

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