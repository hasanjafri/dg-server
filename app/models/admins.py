""" Module represents an Admin. """

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Date, Boolean
)

from sqlalchemy.orm import relationship

from app.models import Base

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, autoincrement=True, primary_key=True)

    email = Column(String(255), nullable=False)
    token_expires = Column(DateTime, nullable=True)
    perishable_token = Column(String(255), nullable=True, unique=True)

    birthday = Column(Date, nullable=True)
    first_name = Column(String(35), nullable=True)
    last_name = Column(String(35), nullable=True)

    is_active = Column(Boolean, default=False)

    project = relationship("Project", uselist=False, back_populates="admin")

    def __repr__(self):
        """ Show admin object info. """
        return '<Admin: {}>'.format(self.id)

    def full_name(self):
        """ Return admin's full name. """
        return '{} {}'.format(self.first_name, self.last_name)

    def formatted_birthday(self):
        """ Return birthday date in a understandable format. """
        return self.birthday.strftime('%m/%d/%Y')