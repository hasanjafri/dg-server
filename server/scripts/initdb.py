import sys
sys.path.append('../')

from sqlalchemy import create_engine

from db.models import Admin
from db.models import Base
from db.models import User

def createDb():
    db_engine = create_engine('postgresql://postgres:admin3@localhost:5432/datagramDb', echo=True, connect_args={'connect_timeout': 10})
    try:
        Base.metadata.create_all(db_engine)
    except Exception:
        raise

if __name__ == "__main__":
    createDb()