from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from db.models.admin import Admin
from db.models.user import User