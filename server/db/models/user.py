from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import column_property, relationship

from db.models import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    #email_address = db.Column(db.String, nullable=False, unique=True)
    fullname = Column(String)
    #password = db.Column(db.String)
    #project_id = db.Column(None, db.ForeignKey('projects.id'))