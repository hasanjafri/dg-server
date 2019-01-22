""" Module for handling all database models.
Notes:
    The models created with the inherited `Base` constant
    must be imported below the declaration for `Alembic`
    autogenerate to work.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.models.users import User
from app.models.admins import Admin
from app.models.projects import Project
from app.models.suppliers import Supplier
from app.models.inventory_products import InventoryProduct
from app.models.categories import Category
from app.models.internal_names import InternalName