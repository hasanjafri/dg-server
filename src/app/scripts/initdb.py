import os
from sqlalchemy import create_engine

from app.models import Base

def createDb():
    db_engine = create_engine(os.environ['DATABASE_URL'], echo=True, connect_args={'connect_timeout': 10})
    try:
        Base.metadata.create_all(db_engine)
    except Exception:
        raise

def clearDb():
    db_engine = create_engine(os.environ['DATABASE_URL'], echo=True, connect_args={'connect_timeout': 10})
    try:
        