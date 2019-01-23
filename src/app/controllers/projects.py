""" Projects controller using Sanic Class based views. """

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.models.projects import Project
from app.models.users import User

class ProjectController(HTTPMethodView):
    """ Handles Project CRUD operations. """

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

    async def get(self, request):
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthorized, please login again'}, status=405)
        else:
            api_key = request['session'].get('DG_api_key')
            account_type = request['session'].get('account_type')
            if await self.valid_api_key(api_key, account_type) == True:
                if account_type == 'admin':
                    with scoped_session() as session:
                        admin = session.query(Admin).filter_by(api_key=api_key).first()
                        projects = session.query(Project).filter_by(admin_id=admin.id)
                        if projects != None:
                            project_list = [project.to_dict() for project in projects]
                            return json({'projects': project_list}, 200)
                        else:
                            return json({'projects': []})
    
    async def post(self, request):
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthenticated'}, status=401)
        else:
            api_key = request['session'].get('DG_api_key')
            account_type = request['session'].get('account_type')
            for param in ['project_name', 'project_address', 'postal_code']:
                if request.json.get(param) == None:
                    return json({'error': 'No {} provided for this request!'.format(param)}, status=400)

            project_name = request.json.get('project_name')
            project_address = request.json.get('project_address')
            postal_code = request.json.get('postal_code')

            if await self.valid_api_key(api_key, account_type) == True:
                with scoped_session() as session:
                    admin = session.query(Admin).filter_by(api_key=api_key).first()
                    project = Project(
                        project_name=project_name,
                        admin_id=admin.id,
                        admin=admin,
                        address=project_address,
                        postal_code=postal_code
                    )
                    session.add(project)

                return json({'msg': 'Project {} was successfully added!'.format(project_name)})
            else:
                return json({'error': 'Unauthenticated'}, status=400)

    async def delete(self, request):
        for param in ['project_name', 'api_key', 'project_id']:
            if request.json.get(param) == None:
                return json({'error': 'No {} provided for this request!'.format(param)}, status=400)

        project_name = request.json.get('project_name')
        api_key = request.json.get('api_key')
        project_id = request.json.get('project_id')

        with scoped_session() as session:
            session.query(Project).filter_by(project_name=project_name)