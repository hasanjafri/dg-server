import datetime

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Float, Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.models import Base
from app.utils.auth import generate_api_key
from app.utils.date_utils import format_datetime_object

class InventoryProduct(Base):
    __table__ = 'inventory_products'

    id = Column(Integer, autoincrement=True, primary_key=True)

    sku = Column(String, nullable=False, unique=True)
    product_name = Column(String, nullable=False)
    unit_size = Column(Float, nullable=False)
    measurement_unit = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)

    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    supplier = relationship("Supplier", back_populates="food_items")