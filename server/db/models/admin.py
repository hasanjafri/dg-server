from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import column_property, relationship

from db.models import Base

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    fullname = Column(String)
    password = Column(String)