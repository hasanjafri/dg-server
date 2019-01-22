import datetime

from sqlalchemy import (
    Column, Integer, String,
    DateTime
)

from sqlalchemy.orm import relationship

from app.models import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, autoincrement=True, primary_key=True)

    category_name = Column(String, nullable=False)
