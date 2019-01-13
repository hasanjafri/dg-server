""" Projects controller using Sanic Class based views. """

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.models.projects import Project

class ProjectController(HTTPMethodView):
    """ Handles Project CRUD operations. """

    async def valid_api_key(self, api_key):
        with scoped_session() as session:
            admin = session.query(Admin).filter_by(api_key=api_key).one()

        if admin.is_active == True:
            return admin
        else:
            return False

    async def get_admin_from_api_key(self, api_key):
        with scoped_session() as session:
            admin = session.query(Admin).filter_by(api_key=api_key).one()
            
        return admin

    async def check_api_key_corresponds_to_id(self, api_key, project_id, project_name):
        admin = await self.get_admin_from_api_key(api_key)
        

    async def get(self, request):
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthorized, please login again'}, status=405)
        else:
            api_key = request['session'].get('DG_api_key')
            if await (self.valid_api_key(api_key)) == True:
                admin = await self.get_admin_from_api_key(api_key)
                with scoped_session() as session:
                    session.query(Project).filter_by(admin_id=admin.id)
    
    async def post(self, request):
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthenticated'})
        else:
            api_key = request['session'].get('DG_api_key')
            for param in ['project_name', 'project_address', 'postal_code']:
                if request.json.get(param) == None:
                    return json({'error': 'No {} provided for this request!'.format(param)}, status=400)

            project_name = request.json.get('project_name')
            project_address = request.json.get('project_address')
            postal_code = request.json.get('postal_code')

            admin = await self.valid_api_key(api_key)

            if admin != False:
                with scoped_session() as session:
                    project = Project(
                        project_name=project_name,
                        admin_id=admin.id,
                        admin=admin,
                        address=project_address,
                        postal_code=postal_code
                    )
                    session.add(project)

                return json({'msg': 'Project {} was succesfully added!'.format(project_name)})
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