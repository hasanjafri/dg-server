""" Suppliers controller using Sanic Class based views. """

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.models.projects import Project
from app.models.suppliers import Supplier
from app.models.users import User

class SupplierController(HTTPMethodView):
    """ Handles Supplier CRUD operations. """

    async def post(self, request):
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthenticated'})
        else:
            api_key = request['session'].get('DG_api_key')
            account_type = request['session'].get('account_type')
            for param in ['project_id', 'name']:
                if request.json.get(param) == None:
                    return json({'error': 'No {} provided for this request!'.format(param)}, status=400)

            project_id = request.json.get('project_id')
            name = request.json.get('name')

            if account_type == 'admin':
                if await self.valid_api_key(api_key, account_type) == True:
                    with scoped_session() as session:
                        project = session.query(Project).filter_by(id=project_id).first()
                        supplier = Supplier(
                            name=name,
                            project=project,
                            project_id=project.id
                        )
                        session.add(supplier)

                    return json({'msg': 'Supplier {} was successfully added!'.format(name)})
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