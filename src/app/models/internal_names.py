import datetime

from sqlalchemy import (
    Column, Integer, String,
    DateTime
)

from app.models import Base

class InternalName(Base):
    __tablename__ = 'internal_names'

    id = Column(Integer, autoincrement=True, primary_key=True)

    internal_name = Column(String, nullable=False)
    