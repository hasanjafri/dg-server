from gino import Gino

db = Gino()

from db.models.admin import Admin
from db.models.user import User