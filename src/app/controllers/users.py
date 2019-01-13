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
        with scoped_session() as session:
            stmt = User.__table__.select()
            users = [dict(u) for u in session.execute(stmt)]
        return json({'users': users})

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
            for param in ['username', 'password', 'project', 'permissions']:
                if request.json.get(param) == None:
                    return json({'error': '{} field cannot be blank!'.format(param)}, status=400)

            username = request.json.get('username')
            (salt, password) = create_password(request.json.get('password'))

            # Create new user.
            with scoped_session() as session:
                user = User(
                    user_name=username,
                    password=password,
                    password_salt=salt,
                    project_id=request.json.get('project_id'),
                    project=project,
                    _permissions=request.json.get('permissions')
                )
                session.add(user)

            # Return json response.
            return json({'msg': 'Successfully created {}'.format(email)})

    async def get_project_by_id(self, project_id):


    async def delete(self, request):
        email = request.json.get('email')

        with scoped_session() as session:
            session.query(User).filter_by(email=email).delete()
            session.commit()

        return json({'msg': 'User with email {} was successfully deleted'.format(email)})