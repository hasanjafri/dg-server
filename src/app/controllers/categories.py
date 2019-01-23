""" Categories controller using Sanic Class based views. """

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.models.categories import Category
from app.models.projects import Project
from app.models.users import User

class CategoryController(HTTPMethodView):
    """ Handles Category CRUD operations. """
    
    async def get(self, request):
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthenticated'}, status=401)
        else:
            api_key = request['session'].get('DG_api_key')
            account_type = request['session'].get('account_type')

    async def post(self, request):
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthenticated'}, status=401)
        else:
            api_key = request['session'].get('DG_api_key')
            account_type = request['session'].get('account_type')

            if request.json.get('category_name') == None or request.json.get('project_id') == None:
                return json({'error': 'No category name or project_id provided for this category'}, status=401)
            
            project_id = request.json.get('project_id')
            category_name = request.json.get('category_name')
            
            if await self.valid_api_key(api_key, account_type) == True:
                if account_type == 'admin':
                    with scoped_session() as session:
                        project = session.query(Project).filter_by(id=project_id).first()
                        category = Category(
                            category_name=category_name,
                            project=project,
                            project_id=project.id
                        )
                        session.add(category)

                    return json({'msg': 'Category {} was successfully added'.format(category_name)})
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