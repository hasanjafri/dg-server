""" Internal naming controller using Sanic Class based views. """

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.models.categories import Category
from app.models.internal_names import InternalName
from app.models.users import User

class InternalNameController(HTTPMethodView):
    """ Handles Internal naming CRUD operations. """
    
    async def post(self, request):
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthenticated'}, status=401)
        else:
            api_key = request['session'].get('DG_api_key')
            account_type = request['session'].get('account_type')

            if request.json.get('category_id') == None or request.json.get('internal_name') == None:
                return json({'error': 'No internal name or category_id provided for this internal name'}, status=400)
            
            category_id = request.json.get('category_id')
            internal_name = request.json.get('internal_name')

            if await self.valid_api_key(api_key, account_type) == True:
                if account_type == 'admin':
                    with scoped_session() as session:
                        category = session.query(Category).filter_by(id=category_id).first()
                        in_name = InternalName(
                            internal_name=internal_name,
                            category=category,
                            category_id=category.id
                        )
                        session.add(in_name)

                    return json({'msg': 'Internal Name {} was successfully added'.format(internal_name)})
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