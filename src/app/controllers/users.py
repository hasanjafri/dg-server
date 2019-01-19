""" Users controller using Sanic Class based views. """
import datetime

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.models.projects import Project
from app.models.users import User
from app.utils.auth import create_password

class UserController(HTTPMethodView):
    """ Handles User CRUD operations. """

    async def get(self, request):
        """ Gets all users in the DB
         Args:
             request (object): contains data pertaining request.
         Notes:
             Realistically There would be some form of authentication in place
             Like a Token to grab the Auth Header value and return a specific
             user based on Token. Although for the purpose of brevity this route
             will just return all users in the database.
         Returns:
             json: containing list of users under the `users` key.
         """
        # Gets all users in DB.
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthorized, please login again'}, status=405)
        else:
            api_key = request['session'].get('DG_api_key')
            account_type = request['session'].get('account_type')
            if account_type == 'admin':
                admin_id = await self.valid_api_key(api_key)
                if admin_id != None:
                    with scoped_session() as session:
                        projects = session.query(Project).filter_by(admin_id=admin_id)
                        if projects != None:
                            return json({'users': [project.users_list() for project in projects]})
                        else:
                            return json({'users': []})
            else:
                return json({'error': 'Unauthorized, please login again'}, status=405)

    async def post(self, request):
        """ Creates a new user based on the `email` key
        Args:
            request (object): contains data pertaining request.
        Returns:
            json: containing key `msg` with success info & email.
        """
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthenticated'})
        else:
            for param in ['username', 'password', 'project_id', 'permissions']:
                if request.json.get(param) == None:
                    return json({'error': '{} field cannot be blank!'.format(param)}, status=400)

            username = request.json.get('username')
            (salt, password) = create_password(request.json.get('password'))
            project_id = request.json.get('project_id')

            with scoped_session() as session:
                project = session.query(Project).filter_by(id=project_id).first()
                user = User(
                    user_name=username,
                    password=password,
                    password_salt=salt,
                    project_id=project.id,
                    project=project,
                    _permissions=request.json.get('permissions')
                )
                session.add(user)

            # Return json response.
            return json({'msg': 'Successfully created User: {}'.format(username)})

    async def delete(self, request):
        email = request.json.get('email')

        with scoped_session() as session:
            session.query(User).filter_by(email=email).delete()
            session.commit()

        return json({'msg': 'User with email {} was successfully deleted'.format(email)})

    async def valid_api_key(self, api_key):
        with scoped_session() as session:
            admin = session.query(Admin).filter_by(api_key=api_key).first()
            if admin != None:
                if admin.is_active == True:
                    return admin.id
                else:
                    return None
            else:
                return None