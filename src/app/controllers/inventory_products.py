""" Inventory Products controller using Sanic Class based views. """

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.models.inventory_products import InventoryProduct
from app.models.suppliers import Supplier
from app.models.users import User

class InventoryProductController(HTTPMethodView):
    """ Handles Inventory Product CRUD operations. """

    async def post(self, request):
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthorized, please login again'}, status=405)
        else:
            api_key = request['session'].get('DG_api_key')
            account_type = request['session'].get('account_type')
            for param in ['sku', 'product_name', 'unit_size', 'measurement_unit', 'quantity', 'cost', 'supplier_id']:
                if request.json.get(param) == None:
                    return json({'error': 'No {} provided for this request!'.format(param)}, status=400)
            
            supplier_id = request.json.get('supplier_id')
            product_name = request.json.get('product_name')

            if account_type == 'admin':
                if await self.valid_api_key(api_key, account_type) == True:
                    with scoped_session() as session:
                        supplier = session.query(Supplier).filter_by(id=supplier_id).first()
                        inventory_product = InventoryProduct(
                            sku=request.json.get('sku'),
                            product_name=product_name,
                            unit_size=request.json.get('unit_size'),
                            measurement_unit=request.json.get('measurement_unit'),
                            quantity=request.json.get('quantity'),
                            cost=request.json.get('cost'),
                            supplier=supplier,
                            supplier_id=supplier.id
                        )
                        session.add(inventory_product)

                    return json({'msg': 'Order {} was successfully added!'.format(product_name)})
                else:
                    return json({'error': 'Unauthenticated'}, status=400)
    
    async def valid_api_key(self, api_key, account_type):
        if account_type == 'admin':
            with scoped_session() as session:
                admin = session.query(Admin).filter_by(api_key=api_key).first()
                if admin != None:
                    if admin.is_active == True:
                        return True
                    else:
                        return None
                else:
                    return None
        elif account_type == 'user':
            with scoped_session() as session:
                user = session.query(User).filter_by(api_key=api_key).first()
                if user != None:
                    if user.is_active == True:
                        return True
                    else:
                        return None
                else:
                    return None
        else:
            return None