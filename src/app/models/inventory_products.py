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
    __tablename__ = 'inventory_products'

    id = Column(Integer, autoincrement=True, primary_key=True)

    sku = Column(String, nullable=False, unique=True)
    product_name = Column(String, nullable=False)
    unit_size = Column(Float, nullable=False)
    measurement_unit = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)

    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    supplier = relationship("Supplier", back_populates="food_items")

    internal_name_id = Column(Integer, ForeignKey('internal_names.id'))
    internal_name = relationship("InternalName", back_populates="_food_items")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        """ Show inventory_product object info. """
        return '<inventoryProduct: {}>'.format(self.product_name)

    def to_dict(self):
        ret = {
            'id': self.id,
            'sku': self.sku,
            'product_name': self.product_name,
            'unit_size': self.unit_size,
            'measurement_unit': self.measurement_unit,
            'quantity': self.quantity,
            'cost': self.cost,
            'supplier_id': self.supplier_id,
            'internal_name_id': self.internal_name_id,
            'created_at': format_datetime_object(self.created_at)
        }
        return ret